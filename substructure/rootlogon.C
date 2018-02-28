#include <TFile.h>
#include <TH2D.h>
void rootlogon() {
  cout << "Ran rootlogon.C" << endl;
}
TFile* f1 = TFile::Open("ddt0.001.root");
TH2D* lookup1 = (TH2D*) f1->Get("lookup");
float ddt01(float n2, float pt, float mass) {
    return n2-lookup1->GetBinContent(max(1,lookup1->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup1->GetYaxis()->FindBin(pt));
}
TFile* f2 = TFile::Open("ddt0.002.root");
TH2D* lookup2 = (TH2D*) f2->Get("lookup");
float ddt02(float n2, float pt, float mass) {
    return n2-lookup2->GetBinContent(max(1,lookup2->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup2->GetYaxis()->FindBin(pt));
}
TFile* f3 = TFile::Open("ddt0.005.root");
TH2D* lookup3 = (TH2D*) f3->Get("lookup");
float ddt05(float n2, float pt, float mass) {
    return n2-lookup3->GetBinContent(max(1,lookup3->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup3->GetYaxis()->FindBin(pt));
}
TFile* f4 = TFile::Open("ddt0.01.root");
TH2D* lookup4 = (TH2D*) f4->Get("lookup");
float ddt1(float n2, float pt, float mass) {
    return n2-lookup4->GetBinContent(max(1,lookup4->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup4->GetYaxis()->FindBin(pt));
}
TFile* f5 = TFile::Open("ddt0.02.root");
TH2D* lookup5 = (TH2D*) f5->Get("lookup");
float ddt2(float n2, float pt, float mass) {
    return n2-lookup5->GetBinContent(max(1,lookup5->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup5->GetYaxis()->FindBin(pt));
}
TFile* f6 = TFile::Open("ddt0.05.root");
TH2D* lookup6 = (TH2D*) f6->Get("lookup");
float ddt5(float n2, float pt, float mass) {
    return n2-lookup6->GetBinContent(max(1,lookup6->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup6->GetYaxis()->FindBin(pt));
}
TFile* f8 = TFile::Open("ddt0.1.root");
TH2D* lookup8 = (TH2D*) f8->Get("lookup");
float ddt10(float n2, float pt, float mass) {
    return n2-lookup8->GetBinContent(max(1,lookup8->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup8->GetYaxis()->FindBin(pt));
}
TFile* f9 = TFile::Open("ddt0.15.root");
TH2D* lookup9 = (TH2D*) f9->Get("lookup");
float ddt15(float n2, float pt, float mass) {
    return n2-lookup9->GetBinContent(max(1,lookup9->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup9->GetYaxis()->FindBin(pt));
}
TFile* f10 = TFile::Open("ddt0.2.root");
TH2D* lookup10 = (TH2D*) f10->Get("lookup");
float ddt20(float n2, float pt, float mass) {
    return n2-lookup10->GetBinContent(max(1,lookup10->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup10->GetYaxis()->FindBin(pt));
}
TFile* f11 = TFile::Open("ddt_n2_b2_0.001.root");
TH2D* lookup11 = (TH2D*) f11->Get("lookup");
float ddtb201(float n2, float pt, float mass) {
    return n2-lookup11->GetBinContent(max(1,lookup11->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup11->GetYaxis()->FindBin(pt));
}
TFile* f12 = TFile::Open("ddt_n2_b2_0.002.root");
TH2D* lookup12 = (TH2D*) f12->Get("lookup");
float ddtb202(float n2, float pt, float mass) {
    return n2-lookup12->GetBinContent(max(1,lookup12->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup12->GetYaxis()->FindBin(pt));
}
TFile* f13 = TFile::Open("ddt_n2_b2_0.005.root");
TH2D* lookup13 = (TH2D*) f13->Get("lookup");
float ddtb205(float n2, float pt, float mass) {
    return n2-lookup13->GetBinContent(max(1,lookup13->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup13->GetYaxis()->FindBin(pt));
}
TFile* f14 = TFile::Open("ddt_n2_b2_0.01.root");
TH2D* lookup14 = (TH2D*) f14->Get("lookup");
float ddtb21(float n2, float pt, float mass) {
    return n2-lookup14->GetBinContent(max(1,lookup14->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup14->GetYaxis()->FindBin(pt));
}
TFile* f15 = TFile::Open("ddt_n2_b2_0.02.root");
TH2D* lookup15 = (TH2D*) f15->Get("lookup");
float ddtb22(float n2, float pt, float mass) {
    return n2-lookup15->GetBinContent(max(1,lookup15->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup15->GetYaxis()->FindBin(pt));
}
TFile* f16 = TFile::Open("ddt_n2_b2_0.05.root");
TH2D* lookup16 = (TH2D*) f16->Get("lookup");
float ddtb25(float n2, float pt, float mass) {
    return n2-lookup16->GetBinContent(max(1,lookup16->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup16->GetYaxis()->FindBin(pt));
}
TFile* f17 = TFile::Open("ddt_n2_b2_0.1.root");
TH2D* lookup17 = (TH2D*) f17->Get("lookup");
float ddtb210(float n2, float pt, float mass) {
    return n2-lookup17->GetBinContent(max(1,lookup17->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup17->GetYaxis()->FindBin(pt));
}
TFile* f18 = TFile::Open("ddt_n2_b2_0.15.root");
TH2D* lookup18 = (TH2D*) f18->Get("lookup");
float ddtb215(float n2, float pt, float mass) {
    return n2-lookup18->GetBinContent(max(1,lookup18->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup18->GetYaxis()->FindBin(pt));
}
TFile* f19 = TFile::Open("ddt_n2_b2_0.2.root");
TH2D* lookup19 = (TH2D*) f19->Get("lookup");
float ddtb220(float n2, float pt, float mass) {
    return n2-lookup19->GetBinContent(max(1,lookup19->GetXaxis()->FindBin(log(pow(mass/pt,2)))),lookup19->GetYaxis()->FindBin(pt));
}
TFile* fkW = TFile::Open("w_pt_spectrum.root");
TGraph* gkNNLOW = (TGraph*) fkW->Get("kNNLO");
float kNNLOW(float pt) {
    return gkNNLOW->Eval(pt);
}
TGraph* gd1kNLOW = (TGraph*) fkW->Get("d1kNLO");
float d1kNLOW(float pt) {
    return gd1kNLOW->Eval(pt);
}
TGraph* gd2kNLOW = (TGraph*) fkW->Get("d2kNLO");
float d2kNLOW(float pt) {
    return gd2kNLOW->Eval(pt);
}
TGraph* gd1kappaEWW = (TGraph*) fkW->Get("d1kappaEW");
float d1kappaEWW(float pt) {
    return gd1kappaEWW->Eval(pt);
}
TGraph* gd2kappaEWW = (TGraph*) fkW->Get("d2kappaEW");
float d2kappaEWW(float pt) {
    return gd2kappaEWW->Eval(pt);
}
TGraph* gdPDFW = (TGraph*) fkW->Get("dPDF");
float dPDFW(float pt) {
    return gdPDFW->Eval(pt);
}
TFile* fkZ = TFile::Open("z_pt_spectrum.root");
TGraph* gkNNLOZ = (TGraph*) fkZ->Get("kNNLO");
float kNNLOZ(float pt) {
    return gkNNLOZ->Eval(pt);
}
TGraph* gd1kNLOZ = (TGraph*) fkZ->Get("d1kNLO");
float d1kNLOZ(float pt) {
    return gd1kNLOZ->Eval(pt);
}
TGraph* gd2kNLOZ = (TGraph*) fkZ->Get("d2kNLO");
float d2kNLOZ(float pt) {
    return gd2kNLOZ->Eval(pt);
}
TGraph* gd1kappaEWZ = (TGraph*) fkZ->Get("d1kappaEW");
float d1kappaEWZ(float pt) {
    return gd1kappaEWZ->Eval(pt);
}
TGraph* gd2kappaEWZ = (TGraph*) fkZ->Get("d2kappaEW");
float d2kappaEWZ(float pt) {
    return gd2kappaEWZ->Eval(pt);
}
TGraph* gdPDFZ = (TGraph*) fkZ->Get("dPDF");
float dPDFZ(float pt) {
    return gdPDFZ->Eval(pt);
}
TFile* n2reweight = TFile::Open("w_jet_wmass_pt_59.root");
TGraph* n2nonpert = new TGraph(((TH1F*)((TCanvas*)n2reweight->Get("c1"))->GetListOfPrimitives()->At(1)));
TGraph* n2 = new TGraph(((TH1F*)((TCanvas*)n2reweight->Get("c1"))->GetListOfPrimitives()->At(2)));
TGraph* raw = new TGraph(((TH1F*)((TCanvas*)n2reweight->Get("c1"))->GetListOfPrimitives()->At(3)));
TGraph* n2detector = new TGraph(((TH1F*)((TCanvas*)n2reweight->Get("c1"))->GetListOfPrimitives()->At(4)));
float weight_n2nonpert(float pt) {
    return n2->Eval(pt)/n2nonpert->Eval(pt);
}
float weight_raw(float pt) {
    return n2->Eval(pt)/raw->Eval(pt);
}
float weight_n2detector(float pt) {
    return n2->Eval(pt)/n2detector->Eval(pt);
}
