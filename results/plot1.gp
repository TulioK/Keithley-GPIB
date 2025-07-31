# Set output to PNG
set terminal pngcairo size 1600,1200 enhanced font 'Verdana,20'
set output 'VI_trueV_Total.png'

# Set graph title and labels
set title "Standard LGAD - Total Current"
set xlabel "Voltage (V)"
set ylabel "Current (nA)"

# Grid for better visibility
set grid
#set key opaque box 
set yrange[-10:150]

# Plot data from a file or directly inline
plot "VI_trueV4.txt" u 2:($4*1e9):3:($5*1e9) w xyerrorbars lw 2 linecolor rgb "red" title "", "VI_trueV4.txt" u 2:($4*1e9) w l lw 2 linecolor rgb "red" notitle




