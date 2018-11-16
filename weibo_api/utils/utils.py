import importlib

from .exception import UnimplementedException


def get_class_from_name(name, module_filename=None):
    cls_name = name.capitalize() if name.islower() else name
    file_name = module_filename or cls_name.lower()
    try:
        imported_module = importlib.import_module(
            '.' + file_name,
            'weibo_api.weibo'
        )
        return getattr(imported_module, cls_name)
    except (ImportError, AttributeError):
        raise UnimplementedException(
            'Unknown weibo obj type [{}]'.format(name)
        )


def build_weibo_obj_from_dict(
        data, session, use_cache=True, cls=None):
    obj_id = data.id
    return cls(obj_id, data if use_cache else None, session)


def get_article_id_from_html(html_content):
    pass
