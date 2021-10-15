# NoonPyMe

![](https://img.shields.io/apm/l/python?style=plastic)

NoonPyMe is an application that provides the user the ability to insert their keyword to the program for scraping products, brands, or sections from noon.com, or by inserting a directed link to the page that you want to scrape.

## Installation

First, make sure that you have Docker installed into your machine before _downloading the version you want to run_.

Second, let's build our docker image (if you modified your module after building your image, you've to re-build it again)

```shell
docker build -t NoonPyMe .
```

Now, let's run the image

```shell
echo "Run the image"
docker run NoonPyMe
echo "Run interactive mode"
docker run -ti NoonPyMe
```

If you want to download the output after finishing scraping

```shell
echo "Run I/O dockor to download written file"
docker run -it --rm -v $(pwd)/directory:/directory NoonPyMe
```

## Versions

- [Version 1.0](https://github.com/DrStarkXavier/NoonPyMe/tree/main/1.0): Main Version of the Application.
- [Version 1.1](https://github.com/DrStarkXavier/NoonPyMe/tree/main/1.1): Fix the maximum Entry level of the products' counter.
- [Version 1.2](https://github.com/DrStarkXavier/NoonPyMe/tree/main/1.2): 
  
  - Change the driver building structure ‒ so, now the use has the ability to call the driver with less time and more mobility.

  - Driver now is the main stream object. So, you don't need to care about re-engineering build setup anymore.

  - Product count is not a static method anymore.

  - Logging timestamp now is located to gmt timestamp.

  - Setup version: 1.2x
  
- [Version 1.3](https://github.com/DrStarkXavier/NoonPyMe/tree/main/1.3):

  - New Feature has been added to the program ‒ now you can search for the keyword of lists of product you would like.

  - Fix the prefix limit amount of scrape – now you're able to scrape 200 products at once, instead of 50 for each.

  - Logging time is now local – according to some demand from users to able to detect their faults.

  - setup version: 1.3x.

## Demo
[![Web Scraping | Data Scraping | noon.com | noonPyMe](https://img.youtube.com/vi/aKtLe3b46xw/0.jpg)](https://www.youtube.com/watch?v=aKtLe3b46xw)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Licence
[Apache License 2.0](https://github.com/DrStarkXavier/NoonPyMe/blob/main/LICENSE)
