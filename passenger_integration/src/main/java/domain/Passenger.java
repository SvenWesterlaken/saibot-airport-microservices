package domain;

public class Passenger {
    private int pass_id;
    private String first_name;
    private String last_name;
    private int is_booker;
    private String email;

    public int getPass_id() {
        return pass_id;
    }

    public void setPass_id(int pass_id) {
        this.pass_id = pass_id;
    }

    public String getFirst_name() {
        return first_name;
    }

    public void setFirst_name(String first_name) {
        this.first_name = first_name;
    }

    public String getLast_name() {
        return last_name;
    }

    public void setLast_name(String last_name) {
        this.last_name = last_name;
    }

    public int getIs_booker() {
        return is_booker;
    }

    public void setIs_booker(int is_booker) {
        this.is_booker = is_booker;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("Passenger [passengerId=");
        builder.append(pass_id);
        builder.append(", passengerFirstName=");
        builder.append(first_name);
        builder.append(", passengerLastName=");
        builder.append(last_name);
        builder.append(", isBooker=");
        builder.append(is_booker);
        builder.append(", email=");
        builder.append(email);
        builder.append("]");
        return builder.toString();
    }
}
