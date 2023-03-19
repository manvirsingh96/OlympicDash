# OlympicDash 🥇

## Table of contents

- [Motivation](#motivation)
- [Explore the app](#explore-the-app)
- [Description](#description)
- [About the data](#about-the-data)
- [Installation](#installation)
- [Contributing](#contributing)

## Motivation

This app can be used as a supplementary app to the [OlymPulse app](https://tetrahydrofuran.shinyapps.io/olympulse/). The OlymPulse app aims to look at the performance of nations over the course of the olympics based on specific sports,  year of competition and the olympic season (winter/summer). This app on the other hand focuses on looking at the performance of the nations based on demographic factors like age, height, weight and sex. As such, this app can be used in conjuction with the OlymPulse to see what demographic factors help in getting more medals as well as how much of a disparity is there in the performance of male and female athletes in different sports.

## Explore the app

**UPDATE THIS You can access the deployed app on [shinyapps.io here](https://tetrahydrofuran.shinyapps.io/olympulse/)!**

## Description and usage

![](img/Olympulse_demo_2.gif)

The app contains two tabs:

1. `Country Level Overview` includes an interactive map that allows the users to click into each country and view the country's records in both Summer and Winter Olympic Games, furthermore, showcases the most successful sport for each country in the history of the Olympic Games. In the side panel, there is a double-sided slider that allows the users to select the range of years they are interested in from 1896 to 2016. There are three menus that enable the users to select their country of interest (as an alternative way to using the interactive map), their sport of interest, and their season of interest (Summer or Winter). With the options selected, the users can view the trend (a line chart) in the total number of medals over the given period of time, the top five medal-winning years, and the medal count by type.

2. `Medal Tally Breakdown` similar to the first tab, includes a double-sided slider that allows the users to select the range of years in addition to three menus that enable the users to select their country of interest, their season of interest, the medal type, sport and event. This section contains a table showing the medals by sport and a treemap showing the main sports.

## About the data

This was created using a historical dataset on the modern Olympic Games athletes, including both Summer and Winter games from Athens 1896 to Rio 2016. The dataset contains 271,116 registers including both medal winners and non-winners. However, we will focus on athletes who won an Olympic medal (39,783 records).

The data set is public and can be found in [tidytuesday](https://github.com/rfordatascience/tidytuesday). Follow this link to access to the source dataset [olympics.csv](https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-07-27/olympics.csv).

## Installation

To install `OlymPulse` locally, you can do as follows:

1. Clone this repository to your local directory.

2. Install all the packages required to run this app by executing the following command in your R console:

    ``` bash
    install.packages(c("shiny", "ggplot2", "tidyverse", "plotly", "leaflet", "leaflet.extras", "sf", "countrycode", "RColorBrewer", "treemapify", "bslib", "shinycssloaders", "shinytest2"))
    ```

3. After installing the packages, execute the following command to run the app:

        RScript app.R

4. Copy the address and paste it in your browser to load the dashboard.

## Contributing

Interested in contributing? We are glad you are interested, please check out the [contributing guidelines](https://github.com/UBC-MDS/OlymPulse/blob/main/CONTRIBUTING.md). Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`OlymPulse` was created by Raul Aguilar Lopez, Manvir Kohli and Crystal Geng. The materials of this project are licensed under the MIT License. If re-using/re-mixing please provide attribution and link to this webpage.

## Contributors

Crystal Geng, Manvir Kohli, Raul Aguilar

<a href="https://github.com/UBC-MDS/OlymPulse/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=UBC-MDS/OlymPulse" />
</a>
