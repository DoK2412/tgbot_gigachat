CHECK_USER = "SELECT * FROM users WHERE user_id_telegram = $1"

ADD_USER = "INSERT INTO users(user_name, user_id_telegram, creation_date) VALUES ($1, $2, $3)"

UPPDATA_COUNT = "UPDATE users SET requests = $1 WHERE user_id_telegram = $2"
