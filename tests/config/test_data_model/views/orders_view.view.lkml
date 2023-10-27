view: orders_view {
  sql_table_name: `etl.prod_read_replica.orders_view` ;;

  drill_fields: [id]

  dimension: id {
    primary_key: yes
    description: "Unique ID for each order instance"
    type: number
    sql: ${TABLE}.id ;;
  }

  dimension: last_order_id {
    label: "Last Order ID"
    type: number
    sql: ${TABLE}.last_order_id ;;
    hidden: yes
  }

  dimension: legit_order_sequence {
    description: "A 'legit' order is one that is not refunded nor is it designated as a 'trial' in our DB, the latter of which indicates:
                  an order to influencers or friends/family;
                  an order sent for free to customers as an apology or replacement for an order lost in transit"
    type: number
    sql: ${TABLE}.legit_order_sequence ;;
    hidden: yes
  }

  dimension: legit_order_sequence_reversed {
    description: "A 'legit' order is one that is not refunded nor is it designated as a 'trial' in our DB, the latter of which indicates:
                  an order to influencers or friends/family;
                  an order sent for free to customers as an apology or replacement for an order lost in transit"
    type: number
    sql: ${TABLE}.legit_order_sequence_reversed ;;
    hidden: yes
  }

  dimension: first_or_recurring_legit_order {
    description: "'First' denotes the first legit order; 'recurring' is for any legit order after the first"
    case: {
      when: {
        sql: ${legit_order_sequence} = 1 ;;
        label: "First"
      }
      when: {
        sql: ${legit_order_sequence} > 1 ;;
        label: "Recurring"
      }
      when: {
        sql: ${legit_order_sequence} IS NULL;;
        label: "Not Legit"
      }
      else: "Unknown"
    }
    hidden: yes
  }

  dimension: unit_price_lead_sku {
    description: "Unit price for lead_sku"
    type: number
    sql: ${amount}/100 ;;
    value_format: "$#.00"
    hidden: yes
  }

  dimension: color {
    hidden: yes
    description: "Color assigned to user"
    type: number
    sql: ${TABLE}.color ;;
  }

  dimension: carrier {
    description: "Mail carrier responsible for delivery of package"
    type: string
    sql: ${TABLE}.carrier ;;
  }

  dimension: chargeid {
    description: "ID associated with purchase transaction"
    type: string
    sql: ${TABLE}.chargeid ;;
  }

  #dimension: flavor {
   # type: string
    #sql: ${TABLE}.flavor ;;
  #}

  dimension: gross {
    type: number
    hidden: yes
    sql: ${TABLE}.gross ;;
  }

  dimension: amount {
    type: number
    hidden: yes
    sql: ${TABLE}.amount ;;
  }

  dimension: net_revenue_lead_sku {
    description: "Net revenue for ONLY lead_sku"
    type: number
    sql: ${amount}/100 ;;
    value_format: "$#.00"
    hidden: yes
  }

  dimension: gross_revenue_lead_sku {
    description: "Gross amount charged for ONLY lead_sku on the order"
    type: number
    sql: ${gross} / 100 ;;
    value_format: "$#.00"
    hidden: yes
  }

  dimension: hasshipped {
    description: "Whether or not the order has shipped (Y/N)"
    type: yesno
    hidden: yes
    sql: ${TABLE}.hasshipped ;;
  }

  dimension: isdelivered {
    description: "Whether or not the order has been delivered (Y/N)"
    type: yesno
    hidden: yes
    sql: ${TABLE}.isdelivered ;;
  }

  dimension: isrefunded {
    description: "Whether or not the order has been refunded (Y/N)"
    type: yesno
    sql: ${TABLE}.isrefunded ;;
  }

  dimension: istrial {
    description: "Whether or not the order is a trial order; note- a trial order can be classified as many different things"
    type: yesno
    sql: ${TABLE}.istrial ;;
    hidden: yes
  }

  dimension_group: orderdatetime {
    description: "Time that customer placed the order"
    type: time
    timeframes: [
      raw,
      time,
      date,
      day_of_week,
      day_of_week_index,
      hour_of_day,
      month_name,
      hour,
      week,
      month,
      quarter,
      year,
      fiscal_month_num,
      week_of_year
    ]
    sql: ${TABLE}.orderdatetime ;;
    convert_tz: yes
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

  dimension: ordered_today {
    description: "Boolean of whether user placed an order today (PT)"
    type: yesno
    sql: ${orderdatetime_date} >= ${now_date} ;;
    hidden: yes
  }

  dimension: profile_id {
    description: "Profile ID associated with each order"
    type: number
    sql: ${TABLE}.profile_id ;;
  }

  #dimension: service {
    #description: "Shipping service for the order"
    #type: string
    #sql: ${TABLE}.service ;;
  #}

  dimension: status {
    description: "Status of the order"
    type: string
    sql: ${TABLE}.status ;;
  }

  dimension: recurring_user_periods {
    type: number
    sql: FLOOR(DATE_DIFF(CURRENT_DATE(), ${orderdatetime_date}, DAY) / 30);;
}
  #dimension: subscription_id {
    #description: "ID for user's subscription"
    #type: number
    #sql: ${TABLE}.subscription_id ;;
  #}

  #dimension: tax {
    #description: "Tax on the order"
    #type: number
    #sql: ${TABLE}.tax/100 ;;
    #value_format: "$#.00"
  #}

  #dimension: third_party {
   # type: yesno
    #sql: ${TABLE}.third_party ;;
  #}

  dimension: trackingnumber {
    description: "Tracking number for the order provided by the carrier"
    type: string
    hidden: yes
    sql: ${TABLE}.trackingnumber ;;
  }

  dimension: trackingurl {
    type: string
    sql: ${TABLE}.trackingurl ;;
  }

  dimension: vendor {
    description: "Payment processing vendor"
    type: string
    sql: ${TABLE}.vendor ;;
  }

  dimension: add_on_revenue {
    type: number
    sql: ${boost_orders_totals_view.total_boost_net_revenue} / 100 ;;
    hidden: yes
  }

  dimension: last_order_date {
    type: date_time
    sql: MAX(${TABLE}.orderdatetime) ;;
}

  measure: order_count {
    description: "Count of orders"
    type: count_distinct
    sql: ${id} ;;
  }

  measure: average_net_revenue_including_addons {
    type: average
    description: "Average Net Revenue in USD dollars; includes lead_sku and addons"
    sql:  ${net_revenue_lead_sku} + ${add_on_revenue} ;;
    value_format_name: usd
    hidden: yes
  }


  measure: total_net_revenue {
    type: sum
    description: "Net Revenue in USD dollars; DOES NOT include addons"
    sql:  ${net_revenue_lead_sku} +${add_on_revenue} ;;
    hidden: yes
    value_format_name: usd
  }

  measure: total_gross_revenue {
    type: sum
    description: "Gross Revenue in USD dollars; DOES NOT include lead_sku and addons"
    sql:  ${gross_revenue_lead_sku} ;;
    hidden: yes
    value_format_name: usd
  }

  measure: net_revenue_including_addons {
    type: sum
    description: "Net Revenue in USD dollars; includes lead_sku and addons"
    sql:  ((${net_revenue_lead_sku}+ ${add_on_revenue})*1.00)/100 ;;
    value_format_name: usd
    hidden: yes
  }

  measure: gross_revenue_including_addons {
    type: sum
    description: "Gross Revenue in USD dollars; includes lead_sku and addons"
    sql:  ((${gross_revenue_lead_sku}+ ${add_on_revenue})*1.00)/100 ;;
    hidden: yes
    value_format_name: usd
  }

  measure: discount_percent_including_addons {
    type: number
    sql:  (${gross_revenue_including_addons} - ${net_revenue_including_addons}) / ${gross_revenue_including_addons};;
    value_format_name: percent_2
    hidden: yes
  }

  measure: discount_percent {
    type: number
    sql:  (${total_gross_revenue} - ${total_net_revenue}) / ${total_gross_revenue};;
    value_format_name: percent_2
    hidden: yes
  }

  #dimension: discount_percent_dim {
    #type: number
    #sql: if(${gross}>=${amount} and ${gross} > 0,100*(${gross} - ${amount}) / ${gross}, 0);;
    #hidden: yes
  #}

  dimension: discount_percent_tier {
    type: tier
    tiers: [1,11,21,31,41, 51]
    style: integer
    sql:  ${discount_percent_dim} ;;
    hidden: yes
  }

  measure: first_order {
    label: "First Order Date"
    type: date
    sql: MIN(${orderdatetime_raw});;
    convert_tz: no
    hidden: yes
  }

  measure: latest_order {
    label: "Latest Order Date"
    type: date_time
    sql: MAX(${orderdatetime_raw});;
    convert_tz: no
    hidden: no
  }

  measure: distinct_purchasers {
    label: "Distinct Purchasers"
    type: count_distinct
    sql: ${profile_id} ;;
    description: "How many distinct purchasers we have. Based on distinct profile_ids"

  }
  measure: distinct_blog_purchasers {
    label: "Distinct Blog Purchasers"
    type: count_distinct
    sql: ${profile_id} ;;
    description: "How many distinct purchasers we have. Based on distinct profile_ids"
    filters: {
      field: permanent_session_view.entry_page 
      value: "-%blog%"
    }
  }

  measure: distinct_influencer_blog_purchasers {
    label: "Distinct Blog Purchasers"
    type: count_distinct
    sql: ${profile_id} ;;
    description: "How many distinct purchasers we have. Based on distinct profile_ids"
    filters: {
      field: permanent_session_view.entry_page 
      value: "-%blog%"
    }
    filters: [
      permanent_session_view.referrer: "influencer"
    ]
  }

}