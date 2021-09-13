## Changes

- Item 1
- Item 2
- Item 3

## Requests / Responses

**Request**

POST `/products` Creates a new product

```json
{
    "title": "Kite",
    "product_type_id": 1,
    "description": "Red. It flies high.",
    "quantity": 5
}
```

**Response**

HTTP/1.1 201 OK

```json
{
    "id": 54,
    "title": "Kite",
    "product_type_id": 1,
    "description": "Red. It flies high.",
    "quantity": 5
}
```

## Testing

- [ ] git fetch --all and checkout to branch ` `
- [ ] Run 
- [ ] Seed 


## Related Issues

- Fixes #22