library(ggplot2)
library(dplyr)
 
# Create data frame
df <- data.frame(rsa = x, ConSurf_Grade = y)
 
# ---- Clean ConSurf Grades ----
# Round if necessary and convert to integer
df <- df %>%
  mutate(
    ConSurf_Grade = as.integer(round(ConSurf_Grade))
  ) %>%
  filter(
    !is.na(ConSurf_Grade),
    ConSurf_Grade >= 1,
    ConSurf_Grade <= 9
  )
 
# ---- Create RSA bins ----
df <- df %>%
  mutate(
    rsa_bin = cut(
      rsa,
      breaks = seq(0, 100, by = 10),
      include.lowest = TRUE,
      right = FALSE
    )
  )
 
# Remove NA bins
df <- df %>% filter(!is.na(rsa_bin))
 
# Reorder bins low-to-high
df <- df %>%
  mutate(
    rsa_bin = factor(rsa_bin, levels = sort(unique(rsa_bin))),
    # Optional: convert grade to factor for discrete coloring
    ConSurf_Grade_Label = factor(
      ConSurf_Grade,
      levels = 1:9,
      labels = paste("Grade", 1:9)
    )
  )
 
# ---- Plot ----
ggplot(df, aes(x = rsa_bin, y = ConSurf_Grade)) +
  geom_boxplot(
    fill = "#69b3a2",
    color = "gray20",
    outlier.shape = NA,
    width = 0.6
  ) +
  geom_jitter(
    width = 0.2,
    alpha = 0.15,
    color = "black",
    size = 0.8
  ) +
  stat_summary(
    fun = median,
    aes(group = 1),
    geom = "line",
    color = "red",
    size = 1
  ) +
  scale_y_continuous(
    breaks = 1:9,
    labels = paste("Grade", 1:9)
  ) +
  labs(
    title = "ConSurf Grade Distribution Across RSA Bins",
    x = "RSA (%) Bin",
    y = "ConSurf Grade"
  ) +
  theme_minimal(base_size = 13) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    plot.title = element_text(face = "bold", size = 14, hjust = 0.5),
    panel.grid.major.x = element_blank(),
    panel.grid.minor.y = element_blank()
  )
