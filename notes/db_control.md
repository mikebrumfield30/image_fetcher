### Start mongoDB
```bash
brew services start mongodb-community@5.0
```

### Stop mongoDB
```bash
brew services stop mongodb-community@5.0
```

### Export collection
```bash
mongoexport --collection=images_for_review --db=raw  --out=out.json
```

### Import collection
```bash
mongoimport out.json
```