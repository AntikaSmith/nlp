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

  def writeDataset(resultName: String, srcData: List[String], train: Set[String], dev: Set[String], test: Set[String]) = {
    val idZipData = srcData.map(_.split("\t").apply(0)).zip(srcData)
    def filterAndWrite(partName: String, set: Set[String]) = {
      val data = idZipData.filter(tuple => set.contains(tuple._1)).map(_._2)
      writeFile("target/" + resultName + "_" + partName + ".tsv", data)
    }
    filterAndWrite("train", train)
    filterAndWrite("dev", dev)
    filterAndWrite("test", test)
  }

  def splitDataset = {
    val original = readFileAsStringList("BioCreative V.5 training set.txt")
    val annotation = readFileAsStringList("CEMP_BioCreative V.5 training set annot.tsv")
    val docIds = annotation.map(_.split("\t").apply(0)).toSet
    val (trainIds, devAndTest) = util.Random.shuffle(docIds).splitAt((docIds.size * 0.6).toInt)
    val (devIds, testIds) = devAndTest.splitAt((devAndTest.size * 0.5).toInt)

    writeDataset("original", original, trainIds, devIds, testIds)
    writeDataset("annotation", annotation, trainIds, devIds, testIds)
  }
}
