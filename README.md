# OlympicDash

## Table of contents

- [Motivation](#motivation)
- [Explore the app](#explore-the-app)
- [Description and Usage](#description-and-usage)
- [About the data](#about-the-data)
- [Installation](#installation)
- [Contributing](#contributing)

## Motivation

This app can be used as a supplementary app to the [OlymPulse app](https://tetrahydrofuran.shinyapps.io/olympulse/). The OlymPulse app aims to look at the performance of nations over the course of the olympics based on specific sports,  year of competition and the olympic season (winter/summer). This app on the other hand focuses on looking at the performance of the nations based on demographic factors like age, height, weight and sex. As such, this app can be used in conjuction with the OlymPulse to see what demographic factors help in getting more medals as well as how much of a disparity is there in the performance of male and female athletes in different sports.

Here is a link to the [proposal](https://github.com/UBC-MDS/OlymPulse/blob/main/reports/proposal.md) for the OlymPulse app. 

## Explore the app

You can access the deployed OlympicDash app via this [link](https://olympicdash.onrender.com)!

## Description and Usage

![](img/app_demo.gif)

The app has 3 visualizations which are controlled by the widgets on the left side of the page. There are currently 4 widgets which you can use to change/filter the visualization :
  1. **Year Slider**: Allows you to consider only the range of years in which you are interested.
  2. **Country Dropdown**: Allows you to select the coutries for which you want to look at the stats
  3. **Sports Dropdown**: Allows you to choose the sport(s) of interest
  4. **Medal Type**: Allows you to focus on specific categories of medals.

  The 3 visualizations in the dashboard include:
  1. **Medal Count by Sex**: This bar plot allows you to compare the medals won in different sports by male and female athletes.
  
  2. **Age/Height/Weight vs Count of Medals by Sex**: This histogram allows you to see the how the number of medals won by athletes is distirbuted over their age or height or weight, for both male and female athletes. You can choose the demographic variable of interets using the dropdown menu just below the graphs. This can be useful if you want to see what age/height/weight works best for a given sport across male and female athletes.

  3. **Trend in Count of Medals by Sex**: This line plot allows you to see how the medaly tally of male and female athletes has changed over time and idenitfy if there is any sport in which there has been an steady inclince or decline in terms of the medals earned.

**Please note that all the visualizations are faceted by country i.e. if you select multiple countries, each vizualization will be broken down into sub-visualizations by country.**
## About the data

Since this app is meant to be supplementary to the OlymPulse app, it uses the same data as the OlymPulse app. You can read about how the data was sourced in OlymPulse's [GitHub repository](https://github.com/UBC-MDS/OlymPulse#about-the-data).

## Installation

To install `OlympicDash` locally, follow the steps below:

1. Clone this repository to your local directory.

2. While in the root directory of the repository , create an environment (using the `od_env.yaml` file) by running the commands below in the terminal. 

    ``` bash
    conda env create -f od_env.yaml
    ```

3. This will create an environment with the name 'olympicdash' install all the packages required to runthe app. Activate the environment by running the following command in terminal:

  ```bash
  conda activate olympicdash
  ```

4. Execute the following command below in terminal to run the app:

        python app.py

5. Click on the link generated in terminal or copy and paste it in your browser to load the dashboard.

## Contributing

Interested in contributing? We are glad you are interested, please check out the [contributing guidelines](https://github.com/manvirsingh96/OlympicDash/blob/main/CONTRIBUTING.md). Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`OlympicDash` was created by Manvir Kohli. The materials of this project are licensed under the MIT License. If re-using/re-mixing please provide attribution and link to this webpage.

## Contributors
 Manvir Kohli