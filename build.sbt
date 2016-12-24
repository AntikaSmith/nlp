name := "nlp"

version := "1.0"

scalaVersion := "2.11.8"

resolvers ++= Seq(
	"maven repository" at "http://repo1.maven.org/maven2"
)

libraryDependencies ++= {
  val SparkVersion = "2.0.0"
  Seq(
  	"edu.stanford.nlp" % "stanford-corenlp" % "3.6.0",
    "uk.ac.cam.ch.wwmm" % "chemicalTagger" % "1.4.0",
    "org.slf4j" % "slf4j-api" % "1.7.5",
    "org.slf4j" % "slf4j-log4j12" % "1.7.5"
  )
}