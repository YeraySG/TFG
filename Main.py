# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 18:29:47 2019

Main file used to call the functions to run the code

@author: u114293
"""

import matplotlib.pyplot as plt
from Functions import readwav, STFTcomputation,InverseSTFT, AutoCorr, CrossCorr, CrossCorrCoeff, AlphaCom, EqualRatios,AddNoise,CnstPwrPanning,Audiowrite,AmbienceEqualLevels,EqLevelMask,EqualLevels
import numpy as np
import scipy.signal as sp

AmbiencePath = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\AudioResults\\EqualRatios\\Ambience\\'
DirectPath = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\AudioResults\\EqualRatios\\Direct\\'
AmbienceElPath = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\AudioResults\\EqualLevels\\Ambience\\'
DirectElPath = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\AudioResults\\EqualLevels\\Direct\\'

#Xl,Xr,Samplerate= readwav('speech-female_Stereo_Lowered.wav')
# Xl,Xr,Samplerate= readwav('R&T.wav')
Xl,Xr,Samplerate= readwav('Fleetwood Mac - Dreams.wav')
#Xl = Xl[:20*Samplerate]
#Xr = Xr[:20*Samplerate]

'Check for zeros'

NewXl = AddNoise (Xl)
NewXr = AddNoise (Xr)

plt.figure()
plt.plot(NewXl, label='Left Chanel Signal')
plt.plot(NewXr, label='Right Chanel Signal')
plt.title('Input signal')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.legend()
plt.show()

'Panning'
#PAudio,PXl,PXr = CnstPwrPanning(NewXl,0)
#
#
#plt.figure()
#plt.plot(PXr, label='Panned Right Chanel Signal')
#plt.plot(PXl, label='Panned Left Chanel Signal')
#plt.title('Panned signal')
#plt.xlabel('Samples')
#plt.ylabel('Amplitude')
#plt.legend()
#plt.show()

#PannedAudio = Audiowrite(PXr,PXl,Samplerate,'PannedAudio_45.wav')

'STFT and Correlation'

#STFTXl, STFTXr = STFTcomputation(PXl,PXr,Samplerate)
STFTXl, STFTXr = STFTcomputation(NewXl,NewXr,Samplerate)

Rll = AutoCorr (STFTXl,0.7)
Rrr = AutoCorr (STFTXr,0.7)

CrossCorrLR = CrossCorr (STFTXl,STFTXr,0.7)
CCCoefficient = CrossCorrCoeff (CrossCorrLR,Rll,Rrr)


'Equal Ratios of Ambience'

AlphaC = AlphaCom (CCCoefficient)
#np.min(AlphaC)
#np.max(AlphaC)

AmbienceL,DirectL = EqualRatios(AlphaC,STFTXl)
AmbienceR,DirectR = EqualRatios(AlphaC,STFTXr)

#plt.figure(),plt.pcolormesh(np.power(np.abs(AmbienceL),2)),plt.colorbar(),plt.show()
#plt.figure(),plt.pcolormesh(np.power(np.abs(AmbienceR),2)),plt.colorbar(),plt.show()
#plt.figure(),plt.pcolormesh(np.power(np.abs(DirectL),2)),plt.colorbar(),plt.show()
#plt.figure(),plt.pcolormesh(np.power(np.abs(DirectR),2)),plt.colorbar(),plt.show()

IAmbienceL,IAmbienceR = InverseSTFT(AmbienceL,AmbienceR,Samplerate)
IDirectL,IDirectR = InverseSTFT(DirectL,DirectR,Samplerate)

Ambience = Audiowrite(IAmbienceL[1],IAmbienceR[1],Samplerate,AmbiencePath)
Direct = Audiowrite(IDirectL[1],IDirectR[1],Samplerate,DirectPath)

#DirectL = (1-AlphaC)*np.abs(STFTXl)
#DirectR = (1-AlphaC)*np.abs(STFTXr)

plt.figure(),plt.pcolormesh(np.power(np.abs(AmbienceL),2)),plt.colorbar(),plt.show()

'Equal Levels of Ambience'

Ia = AmbienceEqualLevels(Rll,Rrr,CrossCorrLR)
MaskL = EqLevelMask(Ia,Rll)
MaskR = EqLevelMask(Ia,Rrr)

plt.figure(),plt.pcolormesh(MaskL),plt.colorbar(),plt.show()
plt.figure(),plt.pcolormesh(MaskR),plt.colorbar(),plt.show()


AmbienceElL, PrimaryElL = EqualLevels(MaskL,STFTXl)
AmbienceElR, PrimaryElR = EqualLevels(MaskR,STFTXr)

IAmbienceElL,IAmbienceElR = InverseSTFT(AmbienceElL,AmbienceElR,Samplerate)
IPrimaryElL,IPrimaryElR = InverseSTFT(PrimaryElL,PrimaryElR,Samplerate)

AmbienceEl = Audiowrite(IAmbienceElL[1],IAmbienceElR[1],Samplerate,AmbienceElPath)
PrimaryEl = Audiowrite(IPrimaryElL[1],IPrimaryElR[1],Samplerate,DirectElPath)

