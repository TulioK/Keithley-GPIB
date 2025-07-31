# Set output to PNG
set terminal pngcairo size 1600,1200 enhanced font 'Verdana,20'
set output 'VI_trueV_Total.png'

# Set graph title and labels
set title "Standard LGAD - Total Current"
set xlabel "Voltage (V)"
set ylabel "Current (nA)"

# Grid for better visibility
set grid
set key opaque box 
set yrange[-10:200]

# Plot data from a file or directly inline
plot "200_VI_J8_gnuplot.txt" u 2:($4*1e9):3:($5*1e9) w xyerrorbars lw 2 linecolor rgb "red" title "Measurement 1", "200_VI_J8_gnuplot.txt" u 2:($4*1e9) w l lw 2 linecolor rgb "red" notitle,"200_VI_J8_2_gnuplot.txt" u 2:($4*1e9):3:($5*1e9) w xyerrorbars lw 2 linecolor rgb "green" title "Measurement 2", "200_VI_J8_2_gnuplot.txt" u 2:($4*1e9) w l lw 2 linecolor rgb "green" notitle, "200_VI_J8_3.txt" u 2:($4*1e9):3:($5*1e9) w xyerrorbars lw 2 linecolor rgb "blue" title "Measurement 3", "200_VI_J8_3.txt" u 2:($4*1e9) w l lw 2 linecolor rgb "blue" notitle, "200_VI_J8_4-5secondDelay.txt" u 2:($4*1e9):3:($5*1e9) w xyerrorbars lw 2 linecolor rgb "black" title "Measurement 4", "200_VI_J8_4-5secondDelay.txt" u 2:($4*1e9) w l lw 2 linecolor rgb "black" notitle




