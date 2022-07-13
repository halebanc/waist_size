# waist_size
A little program to have the minimal waist of a gaussian beam with the razor blade method ([more info](https://www.umu.se/globalassets/centralwebb/studentwebben/institutioner/institutionen-for-fysik/laserfysik/186917_lab-iii.-instructions.-174901_lab-iii-measurement-of-gaussian-laser-beams-2016.pdf)).


To visualize the intensity curve and have the waist of a specific point the command is
```
python Visualisation.py position.csv 
```
You can see the structure of an csv file, with the file position.csv 

To visualise the curve of dispertion of the beam and have the position and size of the w0 use
```
python CharacterizationGaussianBeam.py
```

You need to have multiple csv files with the syntaxe position_x-ycm.csv where the razor is a x,y cm from the start point.
Files need to bee in the same reporty than the python file.
You can see an example in the folder example.
