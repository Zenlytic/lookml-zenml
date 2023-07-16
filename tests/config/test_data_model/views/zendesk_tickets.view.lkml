view: zendesk_tickets {

  sql_table_name: etl.zendesk.tickets_view;;


  dimension: ticket_id {
    label: "Ticket ID"
    primary_key: yes
    type: number
    sql: ${TABLE}.id ;;
    hidden: no
  }

  dimension_group: generated_timestamp {
    label: "Ticket Generated"
    type: time
    timeframes: [
      raw
      , hour, hour_of_day
      , time
      , date
      , week, day_of_week
      , month, day_of_month
      , quarter
      , year, day_of_year, week_of_year
    ]
    sql: TIMESTAMP_SECONDS(${TABLE}.generated_timestamp);;
    convert_tz: yes
  }

  dimension: satisfaction_rating_score {
    group_label: "Satisfaction Rating"
    label: "Score"
    type: string
    sql: (SELECT score FROM UNNEST([${TABLE}.satisfaction_rating])) ;;
  }

  dimension: satisfaction_rating_reason {
    group_label: "Satisfaction Rating"
    label: "Reason"
    type: string
    sql: (SELECT reason FROM UNNEST([${TABLE}.satisfaction_rating])) ;;
  }

  dimension: satisfaction_rating_id {
    group_label: "Satisfaction Rating"
    label: "ID"
    type: number
    sql: (SELECT id FROM UNNEST([${TABLE}.satisfaction_rating])) ;;
    hidden: yes
  }

  dimension: satisfaction_rating_reason_id {
    group_label: "Satisfaction Rating"
    label: "Reason ID"
    type: number
    sql: (SELECT reason_id FROM UNNEST([${TABLE}.satisfaction_rating])) ;;
    hidden: yes
  }

  dimension: satisfaction_rating_comment {
    group_label: "Satisfaction Rating"
    label: "Comment"
    type: string
    sql: (SELECT comment FROM UNNEST([${TABLE}.satisfaction_rating])) ;;
  }

  dimension: url {
    label: "Ticket URL"
    type: string
    sql: ${TABLE}.url ;;
  }

##----- channel dimensions

  dimension: channel_zendesk {
    label: "Original Channel"
    description: "The channel listed by Zendesk; this is hidden to front-end ZD users. We use this when a channel is not identified in the tickets' tags (which might happen when we don't reply)"
    type: string
    sql: ${TABLE}.via.channel ;;
    hidden: no
  }

  dimension: tags {
    type: string
    sql: (SELECT tags_value} FROM UNNEST(${TABLE}.tags)) ;;
    hidden: yes
  }

  dimension: tags_value {
    label: "All Tags"
    description: "A concatenation of each ticket's tags"
    type: string
    sql: (SELECT STRING_AGG(value, ", ") FROM UNNEST(${TABLE}.tags)) ;;
  }

  dimension: channel_tag {
    label: "Tagged Channel"
    type: string
    sql: REGEXP_EXTRACT(${tags_value}, r'(\bemail\b|\bfb_messenger\b|\bvoice__phone_\b|\bzendesk_chat\b|\btrustpilot_review\b|\btypeform/nps\b|\bsms__attentive_\b|\btweet\b)') ;;
    hidden: yes
  }

  dimension: channel_use {
    label: "Channel"
    type: string
    sql:  CASE
            WHEN COALESCE(${channel_tag}, ${channel_zendesk}) = "email"             THEN "Email"
            WHEN COALESCE(${channel_tag}, ${channel_zendesk}) = "fb_messenger"      THEN "FB Messenger"
            WHEN COALESCE(${channel_tag}, ${channel_zendesk}) = "voice__phone_"     THEN "Voice"
            WHEN COALESCE(${channel_tag}, ${channel_zendesk}) = "zendesk_chat"      THEN "Chat"
            WHEN COALESCE(${channel_tag}, ${channel_zendesk}) = "trustpilot_review" THEN "Trustpilot Review"
            WHEN COALESCE(${channel_tag}, ${channel_zendesk}) = "typeform/nps"      THEN "Typeform/NPS"
            WHEN COALESCE(${channel_tag}, ${channel_zendesk}) = "sms__attentive_"   THEN "SMS"
            WHEN COALESCE(${channel_tag}, ${channel_zendesk}) = "tweet"             THEN "Twitter"
            ELSE "Other"
          END;;
    suggestions: ["Email", "FB Messenger", "Voice", "Chat", "Trustpilot Review", "Typeform/NPS", "SMS", "Twitter"]
  }

##-------------------

  dimension: is_merged {
    type: yesno
    sql: REGEXP_EXTRACT(${tags_value}, r'closed_by_merge') ;;
    hidden: yes
  }

  dimension: source_from_address {
    label: "Email Address"
    group_label: "Source: From"
    type: string
    sql: (SELECT address FROM UNNEST([${TABLE}.via.source.from])) ;;
  }

  dimension: source_from_name {
    label: "Name"
    group_label: "Source: From"
    type: string
    hidden: yes
    sql: (SELECT name FROM UNNEST([${TABLE}.via.source.from])) ;;
  }

  dimension: source_from_subject {
    label: "Subject"
    group_label: "Source: From"
    type: string
    hidden: yes
    sql: (SELECT subject FROM UNNEST([${TABLE}.via.source.from])) ;;
  }

  dimension: source_from_ticket_id {
    label: "Ticket ID"
    group_label: "Source: From"
    type: string
    hidden: yes
    sql: (SELECT ticket_id FROM UNNEST([${TABLE}.via.source.from])) ;;
  }

  dimension: source_to_address {
    label: "Email Address"
    group_label: "Source: To"
    type: string
    sql: (SELECT address FROM UNNEST([${TABLE}.via.source.to])) ;;
  }

  dimension: source_to_name {
    label: "Name"
    group_label: "Source: To"
    type: string
    hidden: yes
    sql: (SELECT name FROM UNNEST([${TABLE}.via.source.to])) ;;
  }

  dimension: source_rel {
    type: string
    hidden: yes
    sql: ${TABLE}.via.source.rel;;
  }

  dimension: raw_subject {
    label: "Subject Line"
    type: string
    sql: ${TABLE}.raw_subject ;;
  }

  dimension: recipient {
    type: number
    hidden: no
    sql: ${TABLE}.recipient ;;
  }

  dimension: allow_attachments {
    label: "Tags"
    type: yesno
    sql:${TABLE}.allow_attachments  ;;
    hidden: yes
  }

  dimension_group: created_at {
    label: "Created"
    type: time
    timeframes: [
      raw
      , hour, hour_of_day
      , time
      , date
      , week, day_of_week
      , month, day_of_month
      , quarter
      , year, day_of_year, week_of_year
    ]
    sql: ${TABLE}.created_at ;;
    convert_tz: yes
  }

  dimension_group: updated_at {
    label: "Updated"
    type: time
    timeframes: [
      raw
      , hour, hour_of_day
      , time
      , date
      , week, day_of_week
      , month, day_of_month
      , quarter
      , year, day_of_year, week_of_year
    ]
    sql: ${TABLE}.updated_at ;;
    convert_tz: yes
  }

  dimension: has_incidents {
    type: yesno
    hidden: yes
    sql:${TABLE}.has_incidents ;;
  }

  dimension: allow_channelback {
    description: "Is Channelback Allowed"
    type: yesno
    hidden: yes
    sql:${TABLE}.allow_channelback ;;
  }

  dimension: brand_id {
    label: "Brand ID"
    type: number
    hidden: yes
    sql: ${TABLE}.brand_id ;;
  }

  dimension: collaborator_ids {
    label: "Collaborator IDs"
    type: number
    hidden: yes
    sql: (SELECT value FROM UNNEST(${TABLE}.collaborator_ids)) ;;
  }

  dimension: followup_ids {
    label: "Follow-up IDs"
    type: number
    hidden: yes
    sql: (SELECT value FROM UNNEST(${TABLE}.followup_ids)) ;;
  }

  dimension: group_id {
    label: "Group ID"
    type: number
    sql: ${TABLE}.group_id ;;
  }

  dimension: submitter_id {
    label: "Submitter ID"
    type: number
    sql: ${TABLE}.submitter_id ;;
  }

  dimension: assignee_id {
    label: "Assignee ID"
    hidden: yes
    type: number
    sql: ${TABLE}.assignee_id ;;
  }

  dimension: assigned_rd {
    type: string
    case: {
      when: {
        sql: ${TABLE}.assignee_id = 365435796794
          ;; label: "Matt"
      }
      when: {
        sql: ${TABLE}.assignee_id = 420662816154
          ;; label: "Mary"
      }
      when: {
        sql: ${TABLE}.assignee_id = 428163813074
          ;; label: "Tiffany"
      }
      when: {
        sql: ${TABLE}.assignee_id = 1505717898422
          ;; label: "Laine"
      }
      when: {
        sql: ${TABLE}.assignee_id = 6041537601299
          ;; label: "Edwin"
      }
      when: {
        sql: ${TABLE}.assignee_id = 11792211710227
          ;; label: "Shana"
      }
      when: {
        sql: ${TABLE}.assignee_id = 11792197022995
          ;; label: "Monica"
      }
      }
  }

  dimension: requester_id {
    label: "Requester ID"
    type: number
    sql: ${TABLE}.requester_id ;;
  }

  dimension: subject {
    label: "Ticket Subject"
    type: string
    sql: ${TABLE}.subject ;;
    hidden: yes
  }

  dimension: description {
    type: string
    sql: ${TABLE}.description ;;
  }

  dimension: type {
    label: "Ticket Type"
    type: string
    sql: ${TABLE}.type ;;
    suggestions: ["incident"]
    hidden: yes
  }

  dimension: priority {
    type: string
    sql: ${TABLE}.priority ;;
    hidden: yes
  }

  dimension: organization_id {
    label: "Organization ID"
    type: number
    sql: ${TABLE}.organization_id ;;
    hidden: yes
  }

  dimension: is_public {
    type: yesno
    sql: ${TABLE}.is_public ;;
    hidden: yes
  }

  dimension: status {
    type: string
    sql: ${TABLE}.status ;;
    suggestions: ["new", "open", "solved", "closed", "pending", "hold", "deleted"]
  }

  dimension: rd_tags_consolidated {
    type: string
    sql: if(contains(${rd_ticket_tags.tag}, ${tags_value}), ${rd_ticket_tags.value}, null) ;;
  }

  measure: first_ticket {
    type: date
    sql: MIN(${TABLE}.created_at);;
    convert_tz: no
  }


# follower_ids RECORD
# follower_ids. value INTEGER

# custom_fields.value. id INTEGER
# custom_fields.value. value  STRING
# custom_fields.value. value__bo  BOOLEAN

# custom_fields.value. value__ar  RECORD  REPEATED
# custom_fields.value.value__ar. value  STRING

  dimension: custom_fields {
    sql: ${TABLE}.custom_fields ;;
  }


  measure: has_contacted_rd_before_first_order {
    type: yesno
    sql: (${first_ticket} < ${orders_view.first_order}) OR (${first_ticket} IS NOT NULL AND ${orders_view.first_order} IS NULL) ;;
  }

  measure: 28_days_after_signup {
    hidden: yes
    type: date
    sql: date_add(MIN(${user_view.date_joined_raw}), INTERVAL 28 DAY) ;;
  }

  measure: last_order_before_ticket {
    type: number
    value_format_name: id
    sql:  MAX(CASE WHEN ${orders_view.orderdatetime_raw}   <  ${created_at_raw}  THEN ${orders_view.id}  ELSE NULL END) ;;
  }


  measure: has_contacted_rd_within_28_days_of_sign_up {
    type: yesno
    sql: (${first_ticket} IS NULL AND ${orders_view.first_order} IS NOT NULL) OR (${first_ticket} <= ${28_days_after_signup});;
  }

  measure: count_distinct_tickets {
    type: count_distinct
    sql: ${ticket_id} ;;
    drill_fields: [source_from_address] #ticket_id, created_at_raw, submitter_id, zendesk_users.email
  }

  measure: count_distinct_submitters {
    type: count_distinct
    sql: ${source_from_address} ;;
    drill_fields: [ticket_id, created_at_raw, submitter_id, zendesk_users.email]
  }

}