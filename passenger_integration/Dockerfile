# select image
FROM maven:3-jdk-11

# copy the project files
COPY ./pom.xml ./pom.xml

# build all dependencies for offline use
RUN mvn dependency:go-offline -B

# copy your other files
COPY ./src ./src

# build for release
RUN mvn package

# set the startup command to run your binary
#CMD ["java", "-jar", "./target/passenger_integration-1.0-SNAPSHOT.jar"]
CMD ["mvn", "compile", "exec:java"]
