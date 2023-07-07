1 edit confing in main.py
	
2 run in console
	"C:\Program Files\ParaView 5.10.1-Windows-Python3.9-msvc2017-AMD64\bin\pvpython.exe" 
	
	
	
################## CONFIG
# no trailing slash
data_folder = "U:\\nguyen\\DNSdata_jet\\DNS2_vid"
temp_folder = "C:\\jet_temp" # !! all files will be deleted !!
processed_folder = "Z:\\Nguyen\\jet_pvpython\\processed"
number_frames = 938  # 938 
pv_version = "5.10" #"5.10", "5.8(Does not work)" TODO
temp_save = False
export_format = "cgns" #"cgns", "vtm"
################## CONFIG END



ffmpeg -framerate 30 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p out.mp4



ffmpeg -r 10 -i out%5d.png -pix_fmt yuv420p -vcodec libx264 out.avi

ffmpeg -framerate 30 -i out%5d.png out.mp4
