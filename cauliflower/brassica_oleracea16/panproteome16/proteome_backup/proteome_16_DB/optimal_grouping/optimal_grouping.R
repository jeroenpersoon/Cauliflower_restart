#Assuming the R libraries were installed via Conda, the next line can be ignored. If not, use it to manually install the required package
#install.packages("ggplot2", "~/local/R_libs/", "https://cran.us.r-project.org")
library(ggplot2)

options(warn=-1)

df = read.csv("/lustre/BIF/nobackup/perso009/cauliflower/brassica_oleracea15/panproteome16/proteome_16_DB/optimal_grouping/fn_fp.csv", sep=",", header = TRUE)
plot1 = ggplot(data=df, aes(x=Mode, y=Score, group=Type)) +
    geom_line(aes(color=Type), size = 2) +
    scale_color_manual(values=c("FP" = "#000000", "FN" = "#990000")) +
    theme_classic(base_size = 30) +

    # Remove the legend by switching the uncommented line below
    theme(legend.key.size = unit(1.5, "cm")) +
    #theme(legend.position = "none") + # no legend when this line is uncommented

    scale_y_continuous("Proteins", trans = 'log10', breaks=c(1,10,100,1000,10000,100000,100000,1000000),
                       labels = function(x) format(x, scientific = FALSE)) + # TRUE formats numbers to scientific notation e.g. 1e+00, 1e+01
    scale_x_continuous("Relaxation mode", breaks = 1:8, limits=c(1, 8))

pdf(NULL)
ggsave("/lustre/BIF/nobackup/perso009/cauliflower/brassica_oleracea15/panproteome16/proteome_16_DB/optimal_grouping/optimal_grouping.png", plot= plot1, height = 10, width = 15)
cat("\nPlot written to: /lustre/BIF/nobackup/perso009/cauliflower/brassica_oleracea15/panproteome16/proteome_16_DB/optimal_grouping/optimal_grouping.png\n\n")