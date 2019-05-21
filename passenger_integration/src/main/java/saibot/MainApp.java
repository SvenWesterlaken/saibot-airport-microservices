package saibot;

import domain.Passenger;
import org.apache.camel.CamelContext;
import org.apache.camel.ProducerTemplate;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import java.util.List;

/**
 * A Camel Application
 */
public class MainApp {

//    /**
//     * A main() so we can easily run these routing rules in our IDE
//     */
//    public static void main(String... args) throws Exception {
//        Main main = new Main();
//        main.addRouteBuilder(new MyRouteBuilder());
//        main.run(args);
//    }

    public static void main(String[] args) {

        try {
            ApplicationContext springCtx = new ClassPathXmlApplicationContext(
                    "database-context.xml");

            CamelContext context = springCtx.getBean("passengerCtx", CamelContext.class);

            context.addRoutes(new MyRouteBuilder());

            context.start();

            ProducerTemplate producerTemplate = context.createProducerTemplate();

            // Insert book 1
            Passenger passenger1 = buildPassenger1();
            String resp = producerTemplate.requestBody("direct:insert",  passenger1, String.class);
            System.out.println("resp:"+resp);

            // Insert book 2
            Passenger passenger2 = buildPassenger2();
            resp = producerTemplate.requestBody("direct:insert",  passenger2, String.class);
            System.out.println("resp:"+resp);

            // Read all books
            List<Passenger> resp1 = producerTemplate
                    .requestBody("direct:select",  null, List.class);
            System.out.println("resp1:"+resp1);

        } catch (Exception e) {

            e.printStackTrace();

        }
    }

    private static Passenger buildPassenger1() {

        Passenger passenger = new Passenger();

        passenger.setPass_id(2);
        passenger.setFirst_name("Rogue");
        passenger.setLast_name("Grisham");
        passenger.setEmail("test@gmail.com");
        passenger.setIs_booker(1);
        return passenger;

    }

    private static Passenger buildPassenger2() {

        Passenger passenger = new Passenger();

        passenger.setPass_id(3);
        passenger.setFirst_name("Doctor");
        passenger.setLast_name("King");
        passenger.setEmail("test2@gmail.com");
        passenger.setIs_booker(0);
        return passenger;

    }

}

