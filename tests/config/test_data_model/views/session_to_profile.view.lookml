view: session_to_profile {

  sql_table_name: etl.prod_read_replica.session_to_profile_view ;;

  dimension_group: time_recorded {
    # description: ""
    type: time
    timeframes: [
      raw
      , hour
      , time
      , date
      , week, day_of_week
      , month, day_of_month
      , quarter
      , year, day_of_year, week_of_year
    ]
    sql: ${TABLE}.time_recorded ;;
    convert_tz: no
  }

  dimension: session {
    primary_key: yes
    type: string
    sql: ${TABLE}.session ;;
  }

  dimension: user_id {
    label: "User ID (labeled 'prof_id' in table)"
    type: string
    sql: ${TABLE}.prof_id ;;
  }

  dimension: notes {
    type: string
    sql: ${TABLE}.notes ;;
  }

}