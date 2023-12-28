def get_radar_trend_hover_template():
    '''
        Sets the template for the hover tooltips
        of the radar avarage plot.
        
        Contains four labels, followed by their corresponding
        value and units where appropriate, separated by a
        colon : country, population, GDP and CO2 emissions.
        The labels' font is bold and the values are normal weight
        returns:
            The content of the tooltip
    '''

    hov = '<span style="font-weight:bold;">Time : </span>'+\
          '<span style="font-weight:normal;">%{theta}:00</span>'   +\
          '<span style="font-weight:bold;"><br>Average Variation : </span>'+\
          '<span style="font-weight:normal;">%{r}</span>'   +\
              '<extra></extra>'
    
    return hov

def get_radar_scatter_hover_template():
    '''
        Get the template for the hover tooltips
        of the radar scatter plot.
        returns:
            The content of the tooltip
    '''

    # TODO: Indicate the amount of time the variation has occured
    hov = '<span style="font-weight:bold;">Time : </span>'+\
          '<span style="font-weight:normal;">%{theta}:00</span>'   +\
          '<span style="font-weight:bold;"><br>variation : </span>'+\
          '<span style="font-weight:normal;">%{r}</span>'   +\
          '<span style="font-weight:bold;"><br>Occurences : </span>'+\
          '<span style="font-weight:normal;">%{color} times</span>'   +\
              '<extra></extra>'
    
    return hov