package db.utils;

import domain.Passenger;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class PassengerMapper {

    public Map<String, Object> getMap(Passenger passenger) {
        Map<String, Object> answer = new HashMap<String, Object>();
        answer.put("PASS_ID", passenger.getPass_id());
        answer.put("FIRST_NAME", passenger.getFirst_name());
        answer.put("LAST_NAME", passenger.getLast_name() );
        answer.put("EMAIL", passenger.getEmail());
        answer.put("IS_BOOKER", passenger.getIs_booker());
        return answer;
    }

    public List<Passenger> readPassengers( List<Map<String, Object>> dataList) {

        System.out.println("data:"+dataList);

        List<Passenger> passengers = new ArrayList<Passenger>();

        for (Map<String, Object> data : dataList) {

            Passenger  passenger = new Passenger();

            passenger.setPass_id((Integer) data.get("PASS_ID"));
            passenger.setFirst_name((String) data.get("FIRST_NAME"));
            passenger.setLast_name((String) data.get("LAST_NAME"));
            passenger.setEmail((String) data.get("EMAIL"));
            passenger.setIs_booker((Integer) data.get("IS_BOOKER"));

            passengers.add(passenger);
        }

        return passengers;
    }
}
