# Overview
The Crowd Simulation Program is a software application developed to simulate and assess the risk of larger crowds, specifically addressing the problem of crowd crush incidents. It aims to assist in predicting and preventing future crowd crush incidents by providing a deeper understanding of crowd dynamics, based on the Seoul crowd crush incident.

# Features
- **Representation of Pedestrians**: The program implements moving agents to represent pedestrians in the simulated environment. These agents mimic simple pedestrian behavior, enabling the simulation of crowd movement and dynamics.

- **Visualization of Crowd Movement**: The web application provides visual representations of the crowd's movement through congested spaces. Users can observe the flow of the crowd and identify potential bottlenecks or areas of high congestion.

- **Identification of Risk Areas**: Using cell based crowd density, the program identifies areas with high crowd density and assists in determining the risk of a crowd crush. 

- **Heatmap Visualization**: To aid in risk assessment, the program generates a heatmap of crowd density. The heatmap highlights areas of high density, making it easier to identify potential risk areas.

- **Display of Simulation Data**: The web application displays relevant data related to the simulation, such as crowd density over time. This data visualization helps users analyze trends, patterns, and the risk potential of having a crowd in the simulated space.

*NOTE: the current version is limited to a single layout based on the Itaewon district of Seoul, where the crowd crush incident took place. However other adjustable parameters are available.*

## Roadmap
- **Construction of Custom Scenarios**: The web application will allow users to construct custom spaces to simulate specific scenarios. The user can define the layout, dimensions, obstacles, entrances, and exits of the simulated environment, providing flexibility in testing different crowd dynamics in differen environments.

# Usage
Please follow the instructions provided in [App.API](App.API/README.md) for running the simulation API, and [App.Web](App.Web/README.md) for the web application.