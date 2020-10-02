import pickle
import logging
import os.path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
screen_handler = logging.StreamHandler()
screen_handler.setLevel(logging.DEBUG)
screen_handler.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
                                              datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(screen_handler)


def is_object_exists(obj_path):
    """Check if a object exists on the path

    Returns:
        bool: True for existence, False otherwise
    """

    logger.info('Checking object availability...')
    if os.path.isfile(obj_path):
        logger.info('Object exists!')
        return True
    else:
        logger.warning('Object does not exist!')
        return False


def load_existing_object(obj_path):
    """Load a pickled obj

    Returns:
        obj: Return loaded obj
    """

    with open(obj_path, "rb") as f:
        obj = pickle.load(f)
    logger.info('Object loaded successfully!')
    return obj


def save_object(new_obj, obj_path):
    """Save obj on disk as a pickle file

    Args:
        new_obj (dict): Given obj
        obj_path ():
    """
    try:
        with open(obj_path, 'wb') as pickle_file:
            pickle.dump(new_obj, pickle_file, protocol=2)
        logger.info('Object saved successfully!')
    except (ValueError, KeyError):
        logger.exception('Failed to save the object!')