view: user_view {
  view_label: "User"
  sql_table_name: `etl.prod_read_replica.user_view`
    ;;
  drill_fields: [id]

  dimension: id {
    description: "User ID assigned to each unique user at the time of sign-up"
    primary_key: yes
    type: number
    sql: ${TABLE}.id ;;
  }



  dimension_group: date_joined {
    label: "Joined"
    description: "The date the user completed the quiz and thus created a profile"
    type: time
    timeframes: [
      raw,
      time,
      day_of_week,
      day_of_week_index,
      hour_of_day,
      hour,
      week_of_year,
      date,
      week,
      month,
      quarter,
      year,
    ]
    sql: ${TABLE}.date_joined ;;
  }

  dimension_group: now {
    hidden:  yes
    description: "Time that customer placed the order"
    type: time
    timeframes: [
      raw,
      time,
      date,
      day_of_week,
      hour_of_day,
      week,
      month,
      quarter,
      year,
    ]
    sql: CURRENT_TIMESTAMP() ;;
  }

  dimension: signed_up_today {
    description: "Boolean of whether user finished the quiz today (PT)"
    type: yesno
    hidden: yes
    sql: ${date_joined_date} >= ${now_date} ;;
  }

  dimension: email {
    description: "Email associated with user's profile"
    type: string
    sql: ${TABLE}.email ;;
  }

  dimension: name {
    group_label: "PII"
    description: "Name of the user"
    type: string
    hidden: yes
    sql: ${TABLE}.name ;;
  }

  dimension: Email_Used_for_Personal_Orders {
    type: string
    hidden: yes
    sql: ${TABLE}.Email_Used_for_Personal_Orders ;;
  }

  dimension: is_employee {
    type: yesno
    sql: ${Email_Used_for_Personal_Orders} IS NOT NULL ;;
  }

  dimension: contacted_rd{
    label: "Contacted RD"
    type: yesno
    sql: ${rd_touch_stats.zendesk_users_email} = ${user_view.email} ;;
  }


  measure: count {
    label: "Distinct User Count"
    type: count_distinct
    sql: ${id} ;;
    drill_fields: [id]
  }


  measure: total_converted {
    description: "Total number of users who completed the sign up process at the end of the quiz"
    type: count_distinct
    sql: ${orders_view.profile_id} ;;
  }


  measure: total_converted_within_24_hours {
    description: "count of users that signed up and placed an order within 24 hours"
    type: number
    sql: sum(if(timestamp_diff(${orders_view.orderdatetime_raw}, ${date_joined_raw}, hour) <= 24, 1, 0)) ;;
  }

  measure: total_converted_within_1_hour {
    description: "count of users that signed up and placed an order within 1 hour"
    type: number
    sql: sum(if(timestamp_diff(${orders_view.orderdatetime_raw}, ${date_joined_raw}, hour) <= 1, 1, 0)) ;;
  }

  measure: bottom_of_funnel_conversion_within_24_hours {
    description: "count of users that signed up and placed an order within 24 hours, out of all users that joined on that day"
    type: number
    sql: (${total_converted_within_24_hours}*1.00)/${count} ;;
    value_format_name: percent_2
  }

  measure: bottom_of_funnel_conversion_within_1_hour{
    description: "count of users that signed up and placed an order within 1 hour, out of all users that joined on that day"
    type: number
    sql: (${total_converted_within_1_hour}*1.00)/${count} ;;
    value_format_name: percent_2
  }

  measure: overall_bottom_of_funnel_conversion {
    description: "No time bounds: number of people who purchased divided by number who finished quiz"
    type: number
    sql: (${total_converted}*1.00)/${count} ;;
    value_format_name: percent_2
  }

  #measure: total_converted_within_24_hours {
  #  type: number
  #  sql: sum(if(timestamp_diff(${date_joined_date}, ${orders_view.orderdatetime_date}, HOUR) <= 24, 1, 0)) ;;
  #}

}