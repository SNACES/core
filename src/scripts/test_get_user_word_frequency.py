from pymongo import MongoClient
import bson

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    db = client["Data"]
    collection = db["ProcessedTweets"]

    # query = {"user_id": bson.int64.Int64(939091)}
    query = {}
    map = "function() {"  \
        + "  const user_id = this.user_id;" \
        + "  const text = this.text;" \
        + "  emit(user_id, text)" \
        + "}"

    reduce = "function (key, values) {" \
        + "  const dict = {};" \
        + "  for(value of values) {" \
        + "    for(key of Object.keys(value)) {"\
        + "      if(key in dict) {" \
        + "        dict[key] += value[key];"\
        + "      } else {"\
        + "        dict[key] = value[key];" \
        + "      }" \
        + "    }" \
        + "  }" \
        + "  return dict" \
        + "}"

    result = collection.map_reduce(map=map, reduce=reduce, query=query, out="test_results")
    # for doc in result.find():
    #     print(doc)
