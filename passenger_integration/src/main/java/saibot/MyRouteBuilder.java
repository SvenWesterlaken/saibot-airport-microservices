package saibot;

import domain.Passenger;
import org.apache.camel.Endpoint;
import org.apache.camel.Exchange;
import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.model.dataformat.JsonDataFormat;
import org.apache.camel.model.dataformat.JsonLibrary;

/**
 * A Camel Java DSL Router
 */
public class MyRouteBuilder extends RouteBuilder {

    /**
     * Let's configure the Camel routing rules using Java code...
     */
    public void configure() {

        JsonDataFormat jsonFormat = new JsonDataFormat(JsonLibrary.XStream);
        jsonFormat.setUnmarshalType(Passenger.class);


        from("direct:insert")
                .log("Inserted new Passenger")
                .bean("passengerMapper", "getMap")
                .to("sqlComponent:{{sql.insertPassenger}}");


        from("timer://simpleTimer?period=10000")
                .to("sqlComponent:{{sql.getPassengers}}")
                .marshal(jsonFormat)
                .setHeader(Exchange.HTTP_METHOD, simple("POST"))
                .setHeader(Exchange.CONTENT_TYPE, constant("application/json"))
                .to("http4://flight_management:5000/api/1/flight/5cdc02bbe3dafee2a3538d8e/add_passenger")
                .process(exchange -> log.info("The response code is: {}", exchange.getIn().getHeader(Exchange.HTTP_RESPONSE_CODE)))
        ;

    }

}
