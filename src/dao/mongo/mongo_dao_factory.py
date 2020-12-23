from src.shared.mongo import get_collection_from_config


class MongoDAOFactory():
    def create_getter(config, Type):
        getter = Type()
        collection = get_collection_from_config(config)
        getter.set_collection(collection)

        return getter

    def create_setter(config, Type):
        setter = Type()
        collection = get_collection_from_config(config)
        setter.set_collection(collection)

        return setter
