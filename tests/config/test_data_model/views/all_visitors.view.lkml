view: all_visitors {

  sql_table_name: etl.prod_read_replica.all_visitors_view ;;

  dimension: session_id {
    label: "Session ID"
    primary_key: yes
    type: string
    sql: ${TABLE}.session ;;
  }

  dimension_group: session_time {
    label: "Session"
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
    sql: ${TABLE}.time ;;
    convert_tz: no
  }

  dimension: entry_page {
    type: string
    sql: ${TABLE}.entry_page ;;
  }

  dimension: referrer {
    type: string
    sql: ${TABLE}.referrer ;;
  }

  dimension: device {
    description: "Device type used"
    type: string
    sql: ${TABLE}.device ;;
  }

  dimension: browser {
    description: "Internet browser used"
    type: string
    sql: ${TABLE}.browser ;;
  }

  dimension: operating_system {
    type: string
    sql: ${TABLE}.operating_system ;;
  }

  dimension: is_bot {
    type: yesno
    sql: ${TABLE}.is_bot ;;
  }

  dimension: is_mobile {
    type: yesno
    sql: ${TABLE}.is_mobile ;;
  }

  dimension: utm_content {
    label: "UTM Content"
    type: string
    sql: ${TABLE}.utm_content ;;
  }

  dimension: utm_source {
    label: "UTM Source"
    type: string
    sql: ${TABLE}.utm_source ;;
  }

  dimension: utm_term  {
    label: "UTM Term"
    type: string
    sql: ${TABLE}.utm_term ;;
  }

  dimension: utm_medium {
    label: "UTM Medium"
    type: string
    sql: ${TABLE}.utm_medium ;;
  }

  dimension: utm_campaign {
    label: "UTM Campaign"
    type: string
    sql: ${TABLE}.utm_campaign ;;
  }

  dimension: attribution_source {
    description: "Attribution based on the UTM source"
    case: {
      when: {
        sql: ${utm_source} = "fb" ;;
        label: "Facebook"
      }
      when: {
        sql: ${utm_source} = "ig" ;;
        label: "Facebook"
      }
      when: {
        sql: ${utm_source} = "facebook_organic" ;;
        label: "Facebook"
      }
      when: {
        sql: ${utm_source} = "fybr" ;;
        label: "Facebook"
      }
      when: {
        sql: ${utm_source} = "attentive" ;;
        label: "Facebook"
      }
      when: {
        sql: ${utm_source} = "twilio" ;;
        label: "Facebook"
      }
      when: {
        sql: ${utm_source} = "tapjoy" ;;
        label: "Facebook"
      }
      when: {
        sql: ${utm_source} = "Friendbuy" ;;
        label: "Facebook"
      }
      when: {
        sql: ${utm_source} = "google:brand" ;;
        label: "Google Branded"
      }
      when: {
        sql: ${utm_source} = "google" AND ${utm_campaign} = "SRC:Brand" ;;
        label: "Google Brand"
      }
      when: {
        sql: ${utm_source} = "google" ;;
        label: "Google"
      }
      when: {
        sql: ${utm_source} = "sweatcoin" ;;
        label: "Sweatcoin"
      }
      when: {
        sql: ${utm_source} IS NULL ;;
        label: "Organic"
      }
      else: "Other Source"
    }
  }

 # dimension: city_name {
  #  type: string
   # sql: ${TABLE}.city_name ;;
  #}


  measure: count_distinct_sessions {
    type: count_distinct
    sql: ${session_id} ;;
  }

}