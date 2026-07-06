import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round

# Create a SparkSession
spark = SparkSession.builder.appName("TipsAnalysis").getOrCreate()

# Load the tips.csv dataset
tips_df = spark.read.csv('tips.csv', header=True, inferSchema=True)

# Create Tip_Percentage column
tips_df_with_percentage = tips_df.withColumn(
    "Tip_Percentage",
    round((col("tip") / col("total_bill")) * 100, 2)
)

# Display first 10 records with Tip_Percentage
print("DataFrame with Tip_Percentage column:")
tips_df_with_percentage.show(10)

# Register as temporary SQL view
tips_df_with_percentage.createOrReplaceTempView("tips")

# Find the maximum tip given by gender
max_tip_by_gender = spark.sql("SELECT gender, MAX(tip) as maximum_tip FROM tips GROUP BY gender")
print("\nMaximum tip by gender:")
max_tip_by_gender.show()

# Save the final DataFrame in Parquet format
output_path = "/app/output/tips_with_percentage.parquet" # Save to a dedicated output directory within the container
tips_df_with_percentage.write.mode("overwrite").parquet(output_path)

print(f"\nDataFrame saved to '{output_path}' in Parquet format.")

spark.stop()
print("SparkSession stopped.")