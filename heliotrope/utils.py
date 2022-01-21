from multiprocessing import current_process

is_the_first_process = current_process().name in ["ForkProcess-1", "MainProcess"]
