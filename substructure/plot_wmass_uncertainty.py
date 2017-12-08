from ROOT import *
import ROOT

#gROOT.Macro( os.path.expanduser( '~/rootlogon.C' ) )
gROOT.Reset()
gROOT.SetStyle("Plain")
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.2,"Y")
gStyle.SetPadLeftMargin(0.27)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.10)
gStyle.SetPadRightMargin(0.05)
gStyle.SetMarkerSize(1.5)
gStyle.SetHistLineWidth(1)
gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(505, "XYZ")
gStyle.SetLegendBorderSize(0)

if __name__=="__main__":

  for plot in [1,2,3,4]:
    canvas = TCanvas("","",0,0,300,300)
    #canvas.SetLogy()
    if plot==1:
      entries=[("30/fb",0.27),
             ("300/fb",0.087),
             ("* 3000/fb",0.027),
             ("p_{T}>600 GeV",0.031),
             ("* p_{T}>500 GeV",0.027),
             ("p_{T}>400 GeV",0.017),
             ]
      label="N2<0.25, 50<m<150, W-only"
      umax=300
    if plot==2:
      entries=[("#tau_{21}<0.5",0.046), #21
             ("#tau_{21}<0.4",0.037),
             ("#tau_{21}<0.3",0.032),
             ("#tau_{21}<0.2",0.030),
             ("N2<0.3",0.031), #25
             ("* N2<0.25",0.027),
             ("N2<0.2",0.027),
             ("N2<0.15",0.042),
             ("30<m<130",0.027),
             ("* 50<m<150",0.027),
             ("50<m<130",0.034),
             ("50<m<170",0.028),
             ]
      label="3000/fb, p_{T}>500 GeV, W-only"
      umax=100
    if plot==3:
      entries=[("W-only",0.027),
             ("* W-Z (fix #sigma_{W}/#sigma_{Z})",0.062),
             ("W-Z (loose b cat)",0.051),
             ("W-Z (medium b cat)",0.055),
             ("W-Z (tight b cat)",0.071),
             ]
      label="3000/fb, p_{T}>500 GeV, N2<0.25, 50<m<150"
      umax=100
    if plot==4:
      entries=[("W-Z N2<0.25",0.061),
             ("W-Z DDT N2 1%",0.099),
             ("W-Z DDT N2 2%",0.099),
             ("W-Z DDT N2 3%",0.099),
             ("W-Z DDT N2 4%",0.099),
             ("W-Z DDT N2 5%",0.099),
             ("W-Z DDT N2 6%",0.099),
             ("W-Z DDT N2 8%",0.099),
             ("W-Z DDT N2 10%",0.099),
             ]
      label="3000/fb, p_{T}>500 GeV, 50<m<150"
      umax=100
    entries.reverse()
    hist=TH1F("Wmass",label,len(entries),0,len(entries))
    hist.SetFillColor(4)
    hist.SetBarWidth(0.8)
    hist.SetBarOffset(0.1)
    hist.SetMinimum(0)
    hist.SetMaximum(umax)
    for i in range(len(entries)):
      hist.Fill(entries[i][0],entries[i][1]*1000.)
      hist.GetXaxis().SetBinLabel(i+1,entries[i][0])
    hist.GetYaxis().SetTitle("Statistical W mass uncertainty (MeV)")
    hist.Draw("hbar")

    canvas.SaveAs('Wmass-mmdt-2_'+str(plot)+'.pdf')
    