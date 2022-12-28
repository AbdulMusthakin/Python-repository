itemsToDelete = {
  1: {
  "page1": "item1",
  "page1": "item2",
  "page1": "item3"
  },
  2: {
  "page3": "item1",
  "page3": "item2",
  "page3": "item3"
  },
  3: {
  "page5": "item1",
  "page5": "item2",
  "page5": "item3"
  }
}

contents = {
  1: {
  "page1": "item1",
  "page1": "item2",
  "page1": "item3",
  "page1": "item4",
  "page1": "item5"
  },
  2: {
  "page3": "item1",
  "page3": "item2",
  "page3": "item3"
  },
  3: {
  "page5": "item1",
  "page5": "item2",
  "page5": "item3"
  }
}

for package, package_items in itemsToDelete.items():
    for page, package_item in package_items.items():
        for item in package_item:
            print(item)