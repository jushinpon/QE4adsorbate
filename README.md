1. Make a folder, named data4adsorption, and then put all your data files (you want to manipulate the z coordinates of the adsorbates) in this folder.
2. perl move_adsorbate.pl --> move the adsorbates you assign (example for Li) into the vacuum part and write the data files for generating QE in the next step.
3. perl data2QE4MatCld.pl ---> make QE input files for materials cloud crawling.
4. perl QEinputByMatCld.pl ---> get QE settings by materials cloud
5. perl Final_QEinTrim.pl ---> Modify QE input by some settings from materials cloud
6. perl  ModQEsetting.pl ---> arrange all QE input files into the corresponding foilders for QE calculation
7. perl make_slurm_sh.pl
8. perl submit_allslurm_sh.pl

9. After several hours, perl check_QEjobs.pl 
