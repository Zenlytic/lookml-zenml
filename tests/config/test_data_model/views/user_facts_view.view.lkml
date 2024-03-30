view: profile_facts_view {
  sql_table_name: `etl.prod_read_replica.profile_facts_view`
    ;;

  dimension_group: first_order {
    description: "Date of user's first order"
    type: time
    timeframes: [
      raw,
      time,
      date,
      day_of_week,
      week,
      month,
      quarter,
      year
    ]
    sql: ${TABLE}.first_order_date ;;
  }

  dimension_group: first_ship {
    description: "Date user's first order was shipped"
    type: time
    timeframes: [
      raw,
      time,
      date,
      week,
      month,
      quarter,
      year
    ]
    sql: ${TABLE}.first_ship_date ;;
  }

  dimension: has_colorer_bottle_in_any_order {
    description: "Whether or not the user has a colorer bottle in any order"
    type: yesno
    sql: ${TABLE}.has_colorer_bottle_in_any_order ;;
    hidden: yes
  }

  dimension: has_colorer_bottle_in_first_order {
    description: "Whether or not the user has a colorer bottle in first order"
    type: yesno
    sql: ${TABLE}.has_colorer_bottle_in_first_order ;;
    hidden: yes
  }

  dimension: has_hydration_in_any_order {
    description: "Whether or not the user has a hydration in any order"
    type: yesno
    sql: ${TABLE}.has_hydration_in_any_order ;;
    hidden: yes
  }

  dimension: has_hydration_in_first_order {
    description: "Whether or not the user has a hydration in first order"
    type: yesno
    sql: ${TABLE}.has_hydration_in_first_order ;;
    hidden: yes
  }

  dimension: has_preworkout_in_any_order {
    description: "Whether or not the user has a preworkout in any order"
    type: yesno
    sql: ${TABLE}.has_preworkout_in_any_order ;;
    hidden: no
  }

  dimension: has_preworkout_in_first_order {
    description: "Whether or not the user has a preworkout in first order"
    type: yesno
    sql: ${TABLE}.has_preworkout_in_first_order ;;
    hidden: yes
  }

  dimension: has_water_bottle_in_any_order {
    description: "Whether or not the user has a water bottle in any order"
    type: yesno
    sql: ${TABLE}.has_water_bottle_in_any_order ;;
    hidden: yes
  }

  dimension: has_water_bottle_in_first_order {
    description: "Whether or not the user has a water bottle in first order"
    type: yesno
    sql: ${TABLE}.has_water_bottle_in_first_order ;;
    hidden: yes
  }


  dimension: profile_id {
    primary_key: yes
    description: "Unique id assigned to each user"
    type: number
    hidden: yes
    sql: ${TABLE}.profile_id ;;
  }

  #dimension: sum_orders_six {
    #label: "Six Month Lifetime Orders"
    #description: "orders placed within 6 months of first order"
    #type: number
    #hidden: yes
    #sql: ${TABLE}.sum_orders_six ;;
  #}

  #dimension: sum_orders_three {
    #label: "Three Month Lifetime Orders"
    #description: "orders placed within 3 months of first order"
    #type: number
    #hidden: yes
    #sql: ${TABLE}.sum_orders_three ;;
  #}

  #dimension: sum_orders_twelve {
    #label: "Twelve Month Lifetime Orders"
    #description: "orders placed within 12 months of first order"
    #type: number
    #hidden: yes
    #sql: ${TABLE}.sum_orders_twelve ;;
  #}

  dimension: total_orders {
    description: "sum of user's orders"
    type: number
    hidden: yes
    sql: ${TABLE}.total_orders ;;
  }

  measure: mrr {
    description: "MRR"
    type: sum
    sql: ${TABLE}.mrr ;;
  }

  measure: count_profiles {
    description: "count of profile id's"
    type: count
    drill_fields: [profile_id]
  }

 # measure: average_ltv {
  #  label: "Average Lifetime Value"
  #  description: "the sum amount user has spent during their lifetime divided by the number of users"
  #  type: average
  #  hidden: yes #for now
  #  sql: ${ltv} ;;
  #}

 # measure: average_three_month_LTO {
    #description: "Taking the sum of all orders placed within 3 months for all users and dividing that by the total number of orders"
    #type: average
    #hidden: yes #for now
    #sql: ${sum_orders_three} ;;
  #}

  #measure: average_six_month_LTO {
    #description: " Taking the sum of all orders placed within 6 months for all users and dividing that by the total number of orders"
    #type: average
    #hidden: yes #for now
    #sql: ${sum_orders_six} ;;
  #}

  #measure: average_twelve_month_LTO {
    #description: "Taking the sum of all orders placed within 12 months for all users and dividing that by the total number of orders"
    #type: average
    #hidden: yes #for now
    #sql: ${sum_orders_twelve} ;;
  #}
}