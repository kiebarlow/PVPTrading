import React, { useState } from 'react';
import Slider from '@mui/material/Slider';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

const marks = [
    {
        value: 100,
        label: '100x',
    },
    {
        value: 250,
        label: '250x',
    },
    {
        value: 400,
        label: '400x',
    },
    {
        value: 550,
        label: '550x',
    },
    {
        value: 700,
        label: '700x',
    },
    {
        value: 850,
        label: '850x',
    },
    {
        value: 1000,
        label: '1000x',
    },
];


const AirbnbSlider = styled(Slider)(({ theme }) => ({
    color: '#FFFFFF',
    height: 3,
    padding: '13px 0',

    '& .MuiSlider-track': {
        height: 8,
        background: 'linear-gradient(to right, #00ff00, #ff0000)',
    },
    '& .MuiSlider-rail': {
        color: theme.palette.mode === 'dark' ? '#333333' : '333333',
        opacity: 1,
        height: 8,
    },
    '& .MuiSlider-mark': {
    backgroundColor: 'white', // Make marks white
    width: 5,
    height: 15, // Increase height
    },
    '& .MuiSlider-markActive': {
        backgroundColor: 'currentColor',
    },
    '& .MuiSlider-markLabel': {  // Style for the labels
    fontSize: '0.8rem', // Adjusted font size
    color: 'white', // Labels white
    marginTop: 8, //Added Margin
    },
}));

function AirbnbThumbComponent(props) {
    const {children, ...other} = props;
    return (
        <span {...other}>
      {children}
      <span className="airbnb-bar"/>
      <span className="airbnb-bar"/>
      <span className="airbnb-bar"/>
    </span>
    );
}

export default function CustomizedSlider({onChange}) {
    const [sliderValue, setSliderValue] = useState(100);

    const handleChange = (event, newValue) => {
        setSliderValue(newValue);
        onChange(newValue)
    };

    return (
        <Box sx={{width: '90%'}}>
            <AirbnbSlider
                slots={{thumb: AirbnbThumbComponent}}
                getAriaLabel={(index) => (index === 0 ? 'Minimum price' : 'Maximum price')}
                defaultValue={100}
                step={null} //remove incremental placement
                marks={marks}
                min={100}
                max={1000}
                onChange={handleChange} // Attach onChange event
            />
        </Box>
    );
}

