for file in /home/ubuntu/cop25/*.json; do
  python3 /home/ubuntu/codes/json_to_sql.py "$file"
  echo "$file"
  echo "saved to sql!"
done;
