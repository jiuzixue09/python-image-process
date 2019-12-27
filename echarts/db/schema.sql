DROP TABLE IF EXISTS stats;
CREATE TABLE stats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    board_id INTEGER UNIQUE NOT NULL,
    crawl_rate FLOAT NOT NULL,
    response_success_count INTEGER NOT NULL,
    response_error_count INTEGER NOT NULL,
    request_redirect_count INTEGER NOT NULL,
    page_load_timeout_count INTEGER NOT NULL,
    non_html_response_count INTEGER NOT NULL,
    network_error_count INTEGER NOT NULL,
    filtered_duplicate_item_count INTEGER NOT NULL,
    filtered_item_count INTEGER NOT NULL,
    parse_error_count INTEGER NOT NULL,
    parse_item_count INTEGER NOT NULL,
    date_time DATE NOT NULL,
    run_duration INTEGER NOT NULL,
    create_date_time DATE NOT NULL,
    data_type TEXT NOT NULL
);