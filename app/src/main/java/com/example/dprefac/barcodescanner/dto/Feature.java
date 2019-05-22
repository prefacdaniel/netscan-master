package com.example.dprefac.barcodescanner.dto;

/**
 * Created by dprefac on 22-May-19.
 */

public class Feature {

    private String id;

    private String date;

    private String time_value_sin;

    private String data_len;

    private String irtt;

    private String pachet_number; //TODO NU SCHIMBA

    private String time_value_cos;

    private String client_ip;

    private String source;

    private String total_time;

    private String server_id;

    private String ip_trust_level;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getTime_value_sin() {
        return time_value_sin;
    }

    public void setTime_value_sin(String time_value_sin) {
        this.time_value_sin = time_value_sin;
    }

    public String getData_len() {
        return data_len;
    }

    public void setData_len(String data_len) {
        this.data_len = data_len;
    }

    public String getIrtt() {
        return irtt;
    }

    public void setIrtt(String irtt) {
        this.irtt = irtt;
    }

    public String getPachet_number() {
        return pachet_number;
    }

    public void setPachet_number(String pachet_number) {
        this.pachet_number = pachet_number;
    }

    public String getTime_value_cos() {
        return time_value_cos;
    }

    public void setTime_value_cos(String time_value_cos) {
        this.time_value_cos = time_value_cos;
    }

    public String getClient_ip() {
        return client_ip;
    }

    public void setClient_ip(String client_ip) {
        this.client_ip = client_ip;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public String getTotal_time() {
        return total_time;
    }

    public void setTotal_time(String total_time) {
        this.total_time = total_time;
    }

    public String getServer_id() {
        return server_id;
    }

    public void setServer_id(String server_id) {
        this.server_id = server_id;
    }

    public String getIp_trust_level() {
        return ip_trust_level;
    }

    public void setIp_trust_level(String ip_trust_level) {
        this.ip_trust_level = ip_trust_level;
    }

    @Override
    public String toString() {
        return "ClassPojo [date = " + date + ", time_value_sin = " + time_value_sin + ", data_len = " + data_len + ", irtt = " + irtt + ", pachet_number = " + pachet_number + ", time_value_cos = " + time_value_cos + ", client_ip = " + client_ip + ", id = " + id + ", source = " + source + ", total_time = " + total_time + ", server_id = " + server_id + ", ip_trust_level = " + ip_trust_level + "]";
    }
}
