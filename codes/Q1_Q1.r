# Load necessary libraries
library(dplyr)
library(readr)

# Define file path
file_path <- "/Users/tanerkaragol/Desktop/combined_AlphaMissense_files/W_combined_data.csv"

# Load the CSV file
df <- read_csv(file_path)

# Define column names based on your data
protein_col <- 'Entry name'
position_col <- 'position'
score_col <- 'pathogenicity score'
aa_change_col <- 'a.a.2'

# Filter and deduplicate
df_filtered <- df %>%
  select(all_of(c(protein_col, position_col, score_col, aa_change_col))) %>%
  distinct(across(c(protein_col, position_col, aa_change_col)), .keep_all = TRUE)

# Define the amino acid changes of interest
aa_changes_of_interest <- c('A', 'C', 'F', 'G', 'I', 'L', 'M', 'P', 'V', 'W', 'D', 'E', 'H', 'K', 'N', 'Q', 'R', 'S', 'T', 'Y')
# Filter data for the amino acid changes of interest
df_filtered <- df_filtered %>%
  filter(!!sym(aa_change_col) %in% aa_changes_of_interest)

# Calculate median, Q1, and Q3 for each amino acid change
summary_stats <- df_filtered %>%
  group_by(!!sym(aa_change_col)) %>%
  summarise(
    median_score = median(!!sym(score_col), na.rm = TRUE),
    Q1_score = quantile(!!sym(score_col), 0.25, na.rm = TRUE),
    Q3_score = quantile(!!sym(score_col), 0.75, na.rm = TRUE),
    .groups = 'drop'
  )

# Print results
print(summary_stats)

