# Using the Search Builder

This tool searches the Girder instance using the built search query, and returns results at the collection level. **All comparisons being done are on collections**. The search query will be built through the merging of all search parameters added by the user. To add a search parameter, click the `Add Item` button.

### Format
This tool formats queries to the [Mongo Query Syntax](https://docs.mongodb.com/manual/tutorial/query-documents/). Any query created here is expected to conform to this syntax.

### Types
Each search parameter can have one of four types: `String`, `Number`, `Date`, and `JSON`. These correspond to how the `value` field is interpreted. The `Key` field is always interpreted as `String`.

### Permissions
All search results are filtered to the current Girder user's permission level, so different users may see different results on the same query. Internally, this is using the `findWithPermissions` function in Girder.

### Usage
Clicking the `Search` button with no added search parameters will return all documents visible to the user.

The full path of the key must be specified entirely in the `Key` field. For example, your collection(s) might look something like this:
```
{
  "_accessLevel": 2,
  "_id": "5d35bf56a8d5aada468d0bc2",
  "_modelType": "collection",
  "created": "2019-07-22T13:51:18.143000+00:00",
  "description": "Information about my dinner party",
  "meta": {
    "date": "2019-07-25",
    "location": {
      "address": "37750 Sacramento St",
      "city": "Yolo",
      "state": "California
      "zip": "95697"
    },
    "invited": 10,
    "accepted": 8,
    "guests": [
      "Anna",
      "Bob",
      "Joe",
      "Marie",
      "Frank",
      "Ericka",
      "Richard",
      "Katie"
    ]
  },
  "name": "Dinner Party",
  "public": false,
  "size": 0,
  "updated": "2019-07-23T17:09:05.544000+00:00"
}
```
Then in this case, if you wanted to specify the `address` field, you would set the key as `meta.location.address`. However, if you want to query the root level, on something like `name`, then the key would just be `name`.

#### String
If you wanted to search the `meta.guests` field, you would specify the `Key` as `meta.guests`, and the Value as something like `Bob`, using the `String` type.

#### Number
If you wanted to search the `meta.invited` field, you would supply the corresponding Key and Value, but change the type to `Number`. If you don't change the type, suppling a number like `5` will actually result in `"5"` being used.

#### Date
If you wanted to search the `meta.date` field, you would change the type to `Date`, select a comparison type, and then either type in the date, or use the date-picker to select the date. **The date must be in ISO 8601 format**.

### JSON
The `JSON` field is useful for pasting in existing queries. However, this must be in strict JSON format, including double quotes around all keys. When selecting the `JSON` type, you'll notice that no `Key` field is present. This is because all keys and values are defined within the JSON object provided by the user. This object is merged with the rest of the search parameters.
