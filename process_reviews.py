file_out = open("processed_reviews_2.csv", "w")
i = 1
with open("all_reviews.txt", "r", encoding="utf8") as file:
    for line in file:
        parts = [substring.strip() for substring in line.split('|')]
        file_out.writelines("\"{}\"| \"{}, {}\"\n".format(parts[5], (float(parts[2])-1)/2-1, -((float(parts[3])-1)/2-1)))
        print(i)
        i+=1
file_out.close() 
