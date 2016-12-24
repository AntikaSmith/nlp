/**
  * Created by Anckaro on 2016/12/24.
  */
import uk.ac.cam.ch.wwmm.chemicaltagger.POSContainer;
import uk.ac.cam.ch.wwmm.chemicaltagger.ChemistryPOSTagger;
import uk.ac.cam.ch.wwmm.chemicaltagger.ChemistrySentenceParser;
import uk.ac.cam.ch.wwmm.chemicaltagger.Utils;
import nu.xom.Document;

object ChemicalTagger {
  val testText = """The invention relates to polystyrene-poly (styrene-alternated mannose-based maleic acid), a preparation method thereof and an application of the same, which relates to the polystyrene-poly (styrene-alternated-mannose-based maleic acid) and a medicinal application of the polystyrene-poly (styrene-alternated-mannose-based maleic acid) in the aspects of being taken as an external contraceptive drug and being used for inhibiting HIV-1 infection. The compositions by mass percentage of the polystyrene-poly (styrene-alternated mannose-based maleic acid) are: 30 percent of polystyrene and 70 percent of poly (styrene-alternated-mannose-based maleic acid), wherein, the molecular weight is 22,000. The polystyrene-poly (styrene-alternated mannose-based maleic acid) can be used for preparing the external contraceptive drug and can be used for preparing an external anti-AIDS drug."""
  val trainingData = Preprocess.readFileAsStringList("BioCreative V.5 training set.txt").init.map(_.split("\t").tail)

  def tag(text: String) = {
    val container = ChemistryPOSTagger.getDefaultInstance.runTaggers(text)
    val sentenceParser = new ChemistrySentenceParser(container)
    sentenceParser.parseTags()
    val doc = sentenceParser.makeXMLDocument()
    sentenceParser.printPrettyXML(doc)


    //Utils.writeXMLToFile(doc,"target/file1.xml");
  }

}
