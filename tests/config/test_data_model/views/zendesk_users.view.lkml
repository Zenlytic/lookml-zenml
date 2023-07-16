view: zendesk_users {

  sql_table_name: etl.zendesk.users_view ;;


  dimension: role {
    description: "User role"
    type:  string
    sql: ${TABLE}.role ;;
    suggestions: ["end-user", "agent", "admin"]
  }

  dimension: is_shared_phone_number {
    type: yesno
    sql: ${TABLE}.shared_phone_number ;;
    hidden: yes
  }

  dimension: is_only_private_comments {
    type: yesno
    sql: ${TABLE}.only_private_comments ;;
    hidden: yes
  }

  dimension: url {
    type: string
    sql: ${TABLE}.url ;;
    hidden: yes
  }

  dimension: is_shared_agent {
    type: yesno
    sql: ${TABLE}.shared_agent ;;
    hidden: yes
  }

  dimension: is_report_csv {
    type: yesno
    sql: ${TABLE}.report_csv ;;
    hidden: yes
  }

  dimension: user_id {
    primary_key: yes
    label: "User ID"
    description: "Zendesk's assigned ID for users (for both customers and agents)"
    type: number
    sql: ${TABLE}.id ;;
  }

  dimension: email {
    group_label: "PII"
    type: string
    sql: ${TABLE}.email ;;
  }

  dimension: locale {
    label: "Locale"
    group_label: "PII"
    type: string
    sql: ${TABLE}.locale ;;
    hidden: yes
  }

  dimension: locale_id {
    label: "Locale ID"
    group_label: "PII"
    type: number
    sql: ${TABLE}.locale_id ;;
    hidden: yes
  }

  dimension: phone {
    group_label: "PII"
    type: string
    hidden: yes
    sql: ${TABLE}.phone ;;
  }


  dimension: name {
    group_label: "PII"
    type: string
    hidden: yes
    sql: ${TABLE}.name ;;
  }

  dimension: is_shared {
    type: yesno
    sql: ${TABLE}.shared ;;
    hidden: yes
  }

  dimension: is_verified {
    type: yesno
    hidden: yes
    sql: ${TABLE}.verified ;;
  }

  # dimension:  {
  #   label: ""
  #   description: ""
  #   type:
  #   sql: ${TABLE}. ;;
  #   hidden:
  # }

  dimension: time_zone {
    type: string
    sql: ${TABLE}.time_zone ;;
    hidden: yes
  }

  dimension: organization_id {
    type: number
    sql: ${TABLE}.organization_id ;;
    hidden: yes
  }

  dimension: signature  {
    type: string
    sql: ${TABLE}.signature ;;
    hidden: yes
  }

  dimension: is_moderator  {
    type: yesno
    sql: ${TABLE}.moderator ;;
    hidden: yes
  }

  dimension: is_chat_only  {
    type: yesno
    sql: ${TABLE}.chat_only ;;
    hidden: yes
  }

  dimension: is_restricted_agent  {
    type: yesno
    sql: ${TABLE}.restricted_agent ;;
    hidden: yes
  }

  dimension: is_active  {
    type: yesno
    sql: ${TABLE}.active ;;
    hidden: yes
  }

  dimension: is_suspended  {
    type: yesno
    sql: ${TABLE}.suspended ;;
    hidden: yes
  }

  dimension: is_two_factor_auth_enabled  {
    type: yesno
    sql: ${TABLE}.two_factor_auth_enabled ;;
    hidden: yes
  }

  dimension: ticket_restriction  {
    type: string
    sql: ${TABLE}.ticket_restriction ;;
    hidden: yes
  }

  dimension: details  {
    type: string
    sql: ${TABLE}.details ;;
    hidden: yes
  }

  dimension: alias  {
    type: string
    sql: ${TABLE}.alias ;;
    hidden: yes
  }

  dimension: notes  {
    type: string
    sql: ${TABLE}.notes ;;
    hidden: yes
  }

  dimension: default_group_id  {
    type: number
    sql: ${TABLE}.default_group_id ;;
    hidden: yes
  }

  dimension_group: created_at {
    label: "Created"
    type: time
    timeframes: [
      raw,
      hour_of_day,
      time,
      date,
      week,
      month,
      quarter,
      year
    ]
    sql: ${TABLE}.created_at ;;
    hidden: yes
  }

  dimension_group: updated_at {
    label: "Updated"
    type: time
    timeframes: [
      raw,
      hour_of_day,
      time,
      date,
      week,
      month,
      quarter,
      year
    ]
    sql: ${TABLE}.updated_at ;;
    hidden: yes
  }

  dimension_group: last_login_at {
    label: "Last Login"
    type: time
    timeframes: [
      raw,
      hour_of_day,
      time,
      date,
      week,
      month,
      quarter,
      year
    ]
    sql: ${TABLE}.last_login_at ;;
    hidden: yes
  }

  measure: count_distinct_email_addresses_used {
    hidden: yes
    type: count_distinct
    sql: ${email} ;;
    drill_fields: [zendesk_tickets.ticket_id, zendesk_tickets.created_at_raw, zendesk_tickets.submitter_id, email]
  }

}