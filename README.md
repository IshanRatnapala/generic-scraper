## Generic website scraper

Edit the _scraper.json_ file and run ```python app.py```  
The data will be exported to _export.csv_

## scraper.json

Example _scraper.json_
```
{
    "url": "http://site.toscrape.com",
    "section": {
        "container": {
            "type": "div",
            "class": "element-class",
            "pos": 0 
        },
        "content": {
            "Name": {
                "type": "h4",
                "class": "title-class",
                "pos": 0
            },
            "Category": {
                "type": "div",
                "class": "span5",
                "pos": 0,
                "findByContent": {
                    "findByType": "div",
                    "findByClass": "span1",
                    "withContent": "text inside this div"
                }
            },
            "Languages": {
                "type": "div",
                "class": "span5",
                "pos": 0,
                "findByContent": {
                    "findByType": "div",
                    "findByClass": "span1",
                    "withContent": "text inside this span"
                }
            }
        }
    },
    "next": {
        "container": {
            "type": "div",
            "class": "pagination",
            "pos": 0
        },
        "link": {
            "type": "a",
            "class": "",
            "pos": -2
        }
    }
}
```
---

Key | Value | Description
--- | --- | ---
`url` | Site url | The url of the site to scrape.
`section` | Contains `container` and `content` | Contains `container` and `content`
`container` | `type`, `class` and `pos` | This is what the script will scrape. `container` are the elements that 'contains' the data we want to scrape. The code will iterate through all the elements matching the `container` and extract the data.
`content` | `type`, `class`, `pos` and `findByContent` | This contains the fields we want to scrape. The csv headers will be the keys that are in the `content` node.
`type` | `div`, `span`, etc | The type of element to find.
`class` | class name | The class name of element to find.
`pos` | `0`, `1`, `-1`, `-4` | The index of the element if there are multiple elements matching. Negative values count in reverse.
`findByContent` | Contains `findByType`, `findByClass` and `withContent` | Use this if the element needs to be filtered by some content in the page. Ex: to filter content by a label.
`findByType` | `div`, `span`, etc | The type of element to find.
`findByClass` | class name | The class name of element to find.
`withContent` | String containing the text in the element | Ex. The text of the label.
`next` | Contains `container` and `link`  | This describes the element that holds the link to the next page.
`next[container]` | `type`, `class` and `pos`  | The container that has all the pagination.
`next[link]` | `type`, `class` and `pos`  | The element that contains the link to the next page.  

** All nodes except for `findByContent` are required.

---  


##### Note on `FindByContent`
This node is optional. The element described in `FindByContent` has to be a sibling of the element described in `content`.