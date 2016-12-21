import java.io.PrintWriter

/**
  * Created by Anckaro on 2016/12/20.
  * preprocess the original data, including randomly splitting training/test set and adjudging the data format
  */
object Preprocess {
  def readFileAsStringList(file: String) = {
    val originalStream = getClass.getClassLoader.getResourceAsStream(file)
    val rs = scala.io.Source.fromInputStream(originalStream).getLines().toList
    originalStream.close()
    rs
  }

  def writeFile(name: String, list: List[String]) = {
    val file = new PrintWriter(name)
    list.foreach(s => file.println(s))
    file.close()
  }

  def splitDataset = {
    val original = readFileAsStringList("BioCreative V.5 training set.txt")
    val annotation = readFileAsStringList("CEMP_BioCreative V.5 training set annot.tsv")
    val docIds = annotation.map(_.split("\t").apply(0)).toSet
    val (trainIds, testIds) = util.Random.shuffle(docIds).splitAt((docIds.size * 0.8).toInt)
    println(trainIds.size + "\n" + testIds.size)
    def splitAndWrite(resultName: String, srcData: List[String], train: Set[String], test: Set[String]) = {
      val idZipData = srcData.map(_.split("\t").apply(0)).zip(srcData)
      val trainData = idZipData.filter(tuple => train.contains(tuple._1)).map(_._2)
      val testData = idZipData.filter(tuple => test.contains(tuple._1)).map(_._2)
      writeFile("target/" + resultName + "_train.tsv", trainData)
      writeFile("target/" + resultName + "_test.tsv", testData)
    }

    splitAndWrite("original", original, trainIds, testIds)
    splitAndWrite("annotation", annotation, trainIds, testIds)
  }
}
