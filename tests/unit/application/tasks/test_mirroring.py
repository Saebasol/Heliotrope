# pyright: reportPrivateUsage=false
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from heliotrope.application.tasks.mirroring import (
    MirroringProgress,
    MirroringTask,
    Proxy,
    now,
)
from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.entities.info import Info
from heliotrope.domain.exceptions import GalleryinfoNotFound
from tests.unit.domain.entities.conftest import (
    sample_artist,
    sample_character,
    sample_file,
    sample_galleryinfo,
    sample_group,
    sample_info,
    sample_language,
    sample_language_info,
    sample_language_localname,
    sample_parody,
    sample_raw_galleryinfo,
    sample_raw_language,
    sample_resolved_image,
    sample_tag,
    sample_type,
)


@pytest.fixture
def mock_hitomi_la_repo():
    repo = MagicMock()
    repo.hitomi_la.index_files = ["file1.js", "file2.js"]
    return repo


@pytest.fixture
def mock_sqlalchemy_repo():
    return MagicMock()


@pytest.fixture
def mock_mongodb_repo():
    return MagicMock()


@pytest.fixture
def progress_dict() -> dict[str, Any]:
    return {
        "index_files": [],
        "total": 0,
        "job_total": 0,
        "job_completed": 0,
        "mirrored": 0,
        "is_mirroring_galleryinfo": False,
        "is_converting_to_info": False,
        "is_integrity_checking": False,
        "last_checked": "",
        "last_mirrored": "",
    }


@pytest.fixture
def mirroring_task(
    mock_hitomi_la_repo: MagicMock,
    mock_sqlalchemy_repo: MagicMock,
    mock_mongodb_repo: MagicMock,
    progress_dict: dict[str, Any],
):
    return MirroringTask(
        mock_hitomi_la_repo,
        mock_sqlalchemy_repo,
        mock_mongodb_repo,
        progress_dict,
    )


def test_proxy_init(progress_dict: dict[str, Any]):
    proxy = Proxy(progress_dict)
    assert proxy.progress_dict == progress_dict


def test_proxy_getattr(progress_dict: dict[str, Any]):
    progress_dict["test_key"] = "test_value"
    proxy = Proxy(progress_dict)
    assert proxy.test_key == "test_value"


def test_proxy_setattr(progress_dict: dict[str, Any]):
    proxy = Proxy(progress_dict)
    proxy.new_key = "new_value"
    assert progress_dict["new_key"] == "new_value"
    assert proxy.new_key == "new_value"


def test_proxy_reset(progress_dict: dict[str, Any]):
    proxy = Proxy(progress_dict)
    proxy.job_completed = 10
    proxy.total = 100
    proxy.job_total = 20
    proxy.reset()
    assert proxy.job_completed == 0
    assert proxy.total == 0
    assert proxy.job_total == 0


def test_mirroring_progress_default():
    progress = MirroringProgress.default()
    assert progress.index_files == []
    assert progress.total == 0
    assert progress.job_total == 0
    assert progress.job_completed == 0
    assert progress.mirrored == 0
    assert progress.is_mirroring_galleryinfo is False
    assert progress.is_converting_to_info is False
    assert progress.is_integrity_checking is False
    assert progress.last_checked == ""
    assert progress.last_mirrored == ""


def test_mirroring_progress_reset():
    progress = MirroringProgress.default()
    progress.job_completed = 10
    progress.total = 100
    progress.job_total = 20
    progress.reset()
    assert progress.job_completed == 0
    assert progress.total == 0
    assert progress.job_total == 0


def test_mirroring_task_init(
    mirroring_task: MirroringTask,
    mock_hitomi_la_repo: MagicMock,
    progress_dict: dict[str, Any],
):
    assert mirroring_task.hitomi_la == mock_hitomi_la_repo
    assert mirroring_task.progress.index_files == ["file1.js", "file2.js"]
    assert mirroring_task.skip_ids == set()
    assert mirroring_task.REMOTE_CONCURRENT_SIZE == 50
    assert mirroring_task.LOCAL_CONCURRENT_SIZE == 25


@pytest.mark.asyncio
async def test_preprocess(
    mirroring_task: MirroringTask, sample_galleryinfo: Galleryinfo
):
    async def mock_execute(id: int) -> Galleryinfo:
        galleryinfo = sample_galleryinfo
        galleryinfo.id = 999  # Different ID to test preprocessing
        return galleryinfo

    result = await mirroring_task._preprocess(mock_execute, 12345)
    assert result.id == 12345  # Should be overridden by preprocessing


@pytest.mark.asyncio
async def test_get_differences(mirroring_task: MirroringTask):
    mock_source_usecase = AsyncMock()
    mock_target_usecase = AsyncMock()

    mock_source_usecase.execute.return_value = [1, 2, 3, 4, 5]
    mock_target_usecase.execute.return_value = [3, 4, 5, 6, 7]

    differences = await mirroring_task._get_differences(
        mock_source_usecase, mock_target_usecase
    )
    assert set(differences) == {1, 2}


def test_get_splited_id(mirroring_task: MirroringTask):
    ids = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    size = 3
    result = list(mirroring_task._get_splited_id(ids, size))
    expected = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10,)]
    assert result == expected


def test_get_splited_id_empty(mirroring_task: MirroringTask):
    ids = ()
    size = 3
    result = list(mirroring_task._get_splited_id(ids, size))
    assert result == []


@pytest.mark.asyncio
async def test_process_in_jobs_remote(mirroring_task: MirroringTask):
    ids = (1, 2, 3, 4, 5)
    process_calls = []

    async def mock_process(batch):
        process_calls.append(batch)

    # Store progress values before calling the method (since it resets)
    await mirroring_task._process_in_jobs(ids, mock_process, is_remote=True)

    # Progress is reset at the end, but mirrored should be set
    assert mirroring_task.progress.mirrored == 5
    assert len(process_calls) == 1
    assert process_calls[0] == ids


@pytest.mark.asyncio
async def test_process_in_jobs_local(mirroring_task: MirroringTask):
    ids = tuple(range(1, 51))  # 50 items
    process_calls: list[Any] = []

    async def mock_process(batch):
        process_calls.append(batch)

    await mirroring_task._process_in_jobs(ids, mock_process, is_remote=False)

    # Progress is reset at the end, but mirrored should be set
    assert mirroring_task.progress.mirrored == 50
    assert len(process_calls) == 2


@pytest.mark.asyncio
async def test_fetch_and_store_galleryinfo(
    mirroring_task: MirroringTask, sample_galleryinfo: Galleryinfo
):
    ids = (1, 2, 3)
    mock_target_repo = AsyncMock()

    # Mock GetGalleryinfoUseCase creation and execution
    with patch(
        "heliotrope.application.tasks.mirroring.GetGalleryinfoUseCase"
    ) as mock_get_usecase:
        with patch(
            "heliotrope.application.tasks.mirroring.CreateGalleryinfoUseCase"
        ) as mock_create_usecase:
            # Mock the use case instance
            mock_get_instance = AsyncMock()
            mock_get_instance.execute.return_value = sample_galleryinfo
            mock_get_usecase.return_value = mock_get_instance

            mock_create_instance = AsyncMock()
            mock_create_usecase.return_value = mock_create_instance

            await mirroring_task._fetch_and_store_galleryinfo(ids, mock_target_repo)

            # Should create and execute for each ID
            assert mock_create_instance.execute.call_count == 3


@pytest.mark.asyncio
async def test_fetch_and_store_info(
    mirroring_task: MirroringTask, sample_galleryinfo: Galleryinfo
):
    ids = (1, 2, 3)

    with patch(
        "heliotrope.application.tasks.mirroring.GetGalleryinfoUseCase"
    ) as mock_get_usecase:
        with patch(
            "heliotrope.application.tasks.mirroring.CreateInfoUseCase"
        ) as mock_create_usecase:
            mock_get_instance = AsyncMock()
            mock_get_instance.execute.return_value = sample_galleryinfo
            mock_get_usecase.return_value = mock_get_instance

            mock_create_instance = AsyncMock()
            mock_create_usecase.return_value = mock_create_instance

            await mirroring_task._fetch_and_store_info(ids)

            assert mock_create_instance.execute.call_count == 3


@pytest.mark.asyncio
@patch("heliotrope.application.tasks.mirroring.logger")
async def test_integrity_check_success(
    mock_logger: MagicMock,
    mirroring_task: MirroringTask,
    sample_galleryinfo: Galleryinfo,
):
    ids = (1, 2, 3)

    with patch(
        "heliotrope.application.tasks.mirroring.GetGalleryinfoUseCase"
    ) as mock_get_usecase:
        with patch("heliotrope.application.tasks.mirroring.DeepDiff", return_value={}):
            mock_get_instance = AsyncMock()
            mock_get_instance.execute.return_value = sample_galleryinfo
            mock_get_usecase.return_value = mock_get_instance

            # Mock _preprocess to handle the remote call
            with patch.object(
                mirroring_task, "_preprocess", return_value=sample_galleryinfo
            ):
                await mirroring_task._integrity_check(ids)

                # Should not log any warnings for identical data
                warning_calls = [
                    call
                    for call in mock_logger.warning.call_args_list
                    if "Integrity check failed" in str(call)
                ]
                assert len(warning_calls) == 0


@pytest.mark.asyncio
@patch("heliotrope.application.tasks.mirroring.logger")
async def test_integrity_check_with_differences(
    mock_logger: MagicMock,
    mirroring_task: MirroringTask,
    sample_galleryinfo: Galleryinfo,
):
    ids = (1,)

    with patch(
        "heliotrope.application.tasks.mirroring.GetGalleryinfoUseCase"
    ) as mock_get_usecase:
        with patch(
            "heliotrope.application.tasks.mirroring.DeepDiff",
            return_value={
                "values_changed": {
                    "root['title']": {"old_value": "old", "new_value": "new"}
                }
            },
        ):
            with patch(
                "heliotrope.application.tasks.mirroring.DeleteGalleryinfoUseCase"
            ) as mock_delete_gallery:
                with patch(
                    "heliotrope.application.tasks.mirroring.DeleteInfoUseCase"
                ) as mock_delete_info:
                    with patch(
                        "heliotrope.application.tasks.mirroring.CreateGalleryinfoUseCase"
                    ) as mock_create_gallery:
                        with patch(
                            "heliotrope.application.tasks.mirroring.CreateInfoUseCase"
                        ) as mock_create_info:
                            with patch.object(Info, "from_galleryinfo"):
                                mock_get_instance = AsyncMock()
                                mock_get_instance.execute.return_value = (
                                    sample_galleryinfo
                                )
                                mock_get_usecase.return_value = mock_get_instance

                                mock_delete_gallery_instance = AsyncMock()
                                mock_delete_gallery.return_value = (
                                    mock_delete_gallery_instance
                                )

                                mock_delete_info_instance = AsyncMock()
                                mock_delete_info.return_value = (
                                    mock_delete_info_instance
                                )

                                mock_create_gallery_instance = AsyncMock()
                                mock_create_gallery.return_value = (
                                    mock_create_gallery_instance
                                )

                                mock_create_info_instance = AsyncMock()
                                mock_create_info.return_value = (
                                    mock_create_info_instance
                                )

                                # Mock _preprocess to handle the remote call
                                with patch.object(
                                    mirroring_task,
                                    "_preprocess",
                                    return_value=sample_galleryinfo,
                                ):
                                    await mirroring_task._integrity_check(ids)

                                    # Should log warning and perform delete/create operations
                                    mock_logger.warning.assert_called()
                                    mock_delete_gallery_instance.execute.assert_called_once()
                                    mock_delete_info_instance.execute.assert_called_once()
                                    mock_create_gallery_instance.execute.assert_called_once()
                                    mock_create_info_instance.execute.assert_called_once()


@pytest.mark.asyncio
@patch("heliotrope.application.tasks.mirroring.logger")
async def test_integrity_check_galleryinfo_not_found(
    mock_logger: MagicMock, mirroring_task: MirroringTask
):
    ids = (1,)

    # Mock _preprocess to throw GalleryinfoNotFound
    with patch.object(
        mirroring_task, "_preprocess", side_effect=GalleryinfoNotFound("Not found")
    ):
        await mirroring_task._integrity_check(ids)

        # Should add ID to skip_ids and log warning
        assert 1 in mirroring_task.skip_ids
        mock_logger.warning.assert_called()


@pytest.mark.asyncio
async def test_mirror_with_remote_differences(mirroring_task: MirroringTask):
    remote_ids = (1, 2, 3)

    with patch.object(mirroring_task, "_get_differences") as mock_get_differences:
        with patch.object(mirroring_task, "_process_in_jobs") as mock_process_in_jobs:
            with patch(
                "heliotrope.application.tasks.mirroring.now", return_value="mocked_time"
            ):
                # First call returns remote differences, second call returns empty (no local differences)
                mock_get_differences.side_effect = [remote_ids, ()]

                await mirroring_task.mirror()

                # Should call _process_in_jobs twice (once for galleryinfo, once for integrity check)
                assert mock_process_in_jobs.call_count == 2
                # Since there are no local differences but remote differences exist, last_mirrored should not be set
                assert mirroring_task.progress.last_mirrored == ""


@pytest.mark.asyncio
async def test_mirror_with_local_differences(mirroring_task: MirroringTask):
    local_ids = (4, 5, 6)

    with patch.object(mirroring_task, "_get_differences") as mock_get_differences:
        with patch.object(mirroring_task, "_process_in_jobs") as mock_process_in_jobs:
            # First call returns empty (no remote differences), second call returns local differences
            mock_get_differences.side_effect = [(), local_ids]

            await mirroring_task.mirror()

            # Should call _process_in_jobs twice (once for info conversion, once for integrity check)
            assert mock_process_in_jobs.call_count == 2


@pytest.mark.asyncio
async def test_mirror_no_differences(mirroring_task: MirroringTask):
    with patch.object(mirroring_task, "_get_differences") as mock_get_differences:
        with patch.object(mirroring_task, "_process_in_jobs") as mock_process_in_jobs:
            # Both calls return empty (no differences)
            mock_get_differences.side_effect = [(), ()]

            await mirroring_task.mirror()

            # Should only call _process_in_jobs once for integrity check
            assert mock_process_in_jobs.call_count == 1


@pytest.mark.asyncio
@patch("heliotrope.application.tasks.mirroring.sleep")
@patch("heliotrope.application.tasks.mirroring.logger")
async def test_start_mirroring_single_iteration(
    mock_logger: MagicMock, mock_sleep: MagicMock, mirroring_task: MirroringTask
):
    # Mock sleep to break the infinite loop after first iteration
    call_count = 0

    async def mock_sleep_func(delay):
        nonlocal call_count
        call_count += 1
        if call_count > 1:
            raise Exception("Break loop")

    mock_sleep.side_effect = mock_sleep_func

    with patch.object(mirroring_task, "mirror") as mock_mirror:
        try:
            await mirroring_task.start_mirroring(1.0)
        except Exception as e:
            if str(e) != "Break loop":
                raise

        mock_logger.info.assert_called_with("Starting Mirroring task with delay: 1.0")
        # mirror() should be called at least once
        assert mock_mirror.call_count >= 1
        assert mirroring_task.progress.last_checked != ""


@pytest.mark.asyncio
@patch("heliotrope.application.tasks.mirroring.sleep")
@patch("heliotrope.application.tasks.mirroring.logger")
async def test_start_integrity_check_single_iteration(
    mock_logger: MagicMock, mock_sleep: MagicMock, mirroring_task: MirroringTask
):
    # Mock sleep to break the infinite loop after first iteration
    call_count = 0

    async def mock_sleep_func(delay):
        nonlocal call_count
        call_count += 1
        if call_count > 1:
            raise Exception("Break loop")

    mock_sleep.side_effect = mock_sleep_func

    with patch(
        "heliotrope.application.tasks.mirroring.GetAllGalleryinfoIdsUseCase"
    ) as mock_usecase:
        mock_usecase_instance = AsyncMock()
        mock_usecase_instance.execute.return_value = [1, 2, 3]
        mock_usecase.return_value = mock_usecase_instance

        try:
            await mirroring_task.start_integrity_check(1.0)
        except Exception as e:
            if str(e) != "Break loop":
                raise

        mock_logger.info.assert_called_with(
            "Starting Integrity Check task with delay: 1.0"
        )


@pytest.mark.asyncio
async def test_get_differences_empty_source(mirroring_task: MirroringTask):
    mock_source_usecase = AsyncMock()
    mock_target_usecase = AsyncMock()

    mock_source_usecase.execute.return_value = []
    mock_target_usecase.execute.return_value = [1, 2, 3]

    differences = await mirroring_task._get_differences(
        mock_source_usecase, mock_target_usecase
    )
    assert differences == ()


@pytest.mark.asyncio
async def test_get_differences_empty_target(mirroring_task: MirroringTask):
    mock_source_usecase = AsyncMock()
    mock_target_usecase = AsyncMock()

    mock_source_usecase.execute.return_value = [1, 2, 3]
    mock_target_usecase.execute.return_value = []

    differences = await mirroring_task._get_differences(
        mock_source_usecase, mock_target_usecase
    )
    assert set(differences) == {1, 2, 3}


@pytest.mark.asyncio
async def test_process_in_jobs_empty_ids(mirroring_task: MirroringTask):
    ids = ()
    process_calls = []

    async def mock_process(batch):
        process_calls.append(batch)

    await mirroring_task._process_in_jobs(ids, mock_process, is_remote=True)

    # Progress is reset at the end, but mirrored should be set
    assert mirroring_task.progress.mirrored == 0
    assert len(process_calls) == 0


@pytest.mark.asyncio
@patch("heliotrope.application.tasks.mirroring.logger")
async def test_integrity_check_with_exception_in_preprocess(
    mock_logger: MagicMock, mirroring_task: MirroringTask
):
    ids = (1, 2)

    # Mock _preprocess to throw GalleryinfoNotFound for all IDs
    with patch.object(
        mirroring_task, "_preprocess", side_effect=GalleryinfoNotFound("Not found")
    ):
        await mirroring_task._integrity_check(ids)

        # Both IDs should be added to skip_ids
        assert mirroring_task.skip_ids == {1, 2}
        assert mock_logger.warning.call_count == 2


@pytest.mark.asyncio
async def test_start_mirroring_with_integrity_checking_flag(
    mirroring_task: MirroringTask,
):
    # Set integrity checking flag to True
    mirroring_task.progress.is_integrity_checking = True

    with patch.object(mirroring_task, "mirror") as mock_mirror:
        with patch(
            "heliotrope.application.tasks.mirroring.sleep",
            side_effect=[None, Exception("Break loop")],
        ):
            try:
                await mirroring_task.start_mirroring(0.1)
            except Exception as e:
                if str(e) != "Break loop":
                    raise

            # mirror() should not be called when integrity checking is active
            mock_mirror.assert_not_called()


@pytest.mark.asyncio
async def test_start_integrity_check_with_mirroring_flags(
    mirroring_task: MirroringTask,
):
    # Set mirroring flags to True
    mirroring_task.progress.is_mirroring_galleryinfo = True
    mirroring_task.progress.is_converting_to_info = True

    with patch.object(mirroring_task, "_process_in_jobs") as mock_process_in_jobs:
        with patch(
            "heliotrope.application.tasks.mirroring.sleep",
            side_effect=[None, Exception("Break loop")],
        ):
            try:
                await mirroring_task.start_integrity_check(0.1)
            except Exception as e:
                if str(e) != "Break loop":
                    raise

            # _process_in_jobs should not be called when mirroring is active
            mock_process_in_jobs.assert_not_called()


@pytest.mark.asyncio
async def test_start_integrity_check_with_exception_clears_skip_ids(
    mirroring_task: MirroringTask,
):
    # Add some items to skip_ids
    mirroring_task.skip_ids.add(1)
    mirroring_task.skip_ids.add(2)

    with patch.object(
        mirroring_task, "_process_in_jobs", side_effect=Exception("Test exception")
    ):
        with patch(
            "heliotrope.application.tasks.mirroring.GetAllGalleryinfoIdsUseCase"
        ) as mock_usecase:
            with patch(
                "heliotrope.application.tasks.mirroring.sleep",
                side_effect=[None, Exception("Break loop")],
            ):
                mock_usecase_instance = AsyncMock()
                mock_usecase_instance.execute.return_value = [1, 2, 3]
                mock_usecase.return_value = mock_usecase_instance

                try:
                    await mirroring_task.start_integrity_check(0.1)
                except Exception as e:
                    if str(e) != "Break loop":
                        raise

                # skip_ids should be cleared after exception
                assert mirroring_task.skip_ids == set()


@pytest.mark.asyncio
async def test_preprocess_edge_case_comment(
    mirroring_task: MirroringTask, sample_galleryinfo: Galleryinfo
):
    """Test the edge case mentioned in the comment: 1783616 <=> 1669497"""

    async def mock_execute(id: int) -> Galleryinfo:
        galleryinfo = sample_galleryinfo
        galleryinfo.id = 1669497  # Different ID as mentioned in comment
        return galleryinfo

    result = await mirroring_task._preprocess(mock_execute, 1783616)
    assert result.id == 1783616  # Should be overridden by preprocessing


@pytest.mark.asyncio
async def test_mirror_with_both_differences(mirroring_task: MirroringTask):
    remote_ids = (1, 2, 3)
    local_ids = (4, 5, 6)

    with patch.object(mirroring_task, "_get_differences") as mock_get_differences:
        with patch.object(mirroring_task, "_process_in_jobs") as mock_process_in_jobs:
            with patch(
                "heliotrope.application.tasks.mirroring.now",
                return_value="mocked_time",
            ):
                # First call returns remote differences, second call returns local differences
                mock_get_differences.side_effect = [remote_ids, local_ids]

                await mirroring_task.mirror()

                # Should call _process_in_jobs three times (galleryinfo, info conversion, integrity check)
                assert mock_process_in_jobs.call_count == 3
                assert mirroring_task.progress.last_mirrored == "mocked_time"


@pytest.mark.asyncio
async def test_fetch_and_store_galleryinfo_with_different_target_repo(
    mirroring_task: MirroringTask, sample_galleryinfo: Galleryinfo
):
    ids = (1, 2)
    different_target_repo = AsyncMock()

    with patch(
        "heliotrope.application.tasks.mirroring.GetGalleryinfoUseCase"
    ) as mock_get_usecase:
        with patch(
            "heliotrope.application.tasks.mirroring.CreateGalleryinfoUseCase"
        ) as mock_create_usecase:
            mock_get_instance = AsyncMock()
            mock_get_instance.execute.return_value = sample_galleryinfo
            mock_get_usecase.return_value = mock_get_instance

            mock_create_instance = AsyncMock()
            mock_create_usecase.return_value = mock_create_instance

            await mirroring_task._fetch_and_store_galleryinfo(
                ids, different_target_repo
            )

            # Should create usecase with the provided target repository
            mock_create_usecase.assert_called_with(different_target_repo)
            assert mock_create_instance.execute.call_count == 2
