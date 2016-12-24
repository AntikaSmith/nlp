/**
  * Created by Anckaro on 2016/12/20.
  */
object Main {
  def main(args: Array[String]) = {
    Preprocess.splitDataset
    ChemicalTagger.tag(ChemicalTagger.testText)
  }


}
