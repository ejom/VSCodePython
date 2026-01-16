import pandas as pd
import matplotlib.pyplot as plt

raw_df = pd.read_csv('trainingset_v1d1_metadata.csv')
no_glitch_df = raw_df[raw_df['label']=='No_Glitch']
no_glitch_df.drop(['url1', 'url2', 'url3', 'url4'], axis=1, inplace=True)

#print(no_glitch_df[no_glitch_df['peak_time']!=no_glitch_df['start_time']])

amp_snr_df = no_glitch_df[['peak_time', 'amplitude', 'snr', 'ifo']].sort_values(by='peak_time')

lower_amp = no_glitch_df['amplitude'].mean()
lower_snr = no_glitch_df['snr'].mean()
upper_amp_snr_df = amp_snr_df[(amp_snr_df['amplitude']>lower_amp) & (amp_snr_df['snr']>lower_snr)]

print("Group 1: uppper mean for both")
print(upper_amp_snr_df[['peak_time', 'amplitude', 'snr', 'ifo']])

upper_amp = lower_amp + 3*no_glitch_df['amplitude'].std()
upper_snr = lower_snr + 3*no_glitch_df['snr'].std()
extr_amp_df = amp_snr_df[amp_snr_df['amplitude']>upper_amp]
extr_snr_df = amp_snr_df[amp_snr_df['snr']>upper_snr]

print()
print("Group 2: upper mean+3stdev for either")
print(extr_amp_df[['peak_time', 'amplitude', 'ifo']])
print(extr_snr_df[['peak_time', 'snr', 'ifo']])

spec_amp_df = amp_snr_df[(amp_snr_df['amplitude']>lower_amp) & (amp_snr_df['snr']>lower_snr) & (amp_snr_df['amplitude']>upper_amp)]
spec_snr_df = amp_snr_df[(amp_snr_df['amplitude']>lower_amp) & (amp_snr_df['snr']>lower_snr) & (amp_snr_df['snr']>upper_snr)]

print()
print("Group 3: upper mean for both and upper mean+3stdev for either")
print(spec_amp_df[['peak_time', 'amplitude', 'ifo']])
print(spec_snr_df[['peak_time', 'snr', 'ifo']])

vspec_amp_snr_df = amp_snr_df[(amp_snr_df['amplitude']>upper_amp) & (amp_snr_df['snr']>upper_snr)]
print()
print("Group 4: upper mean+3stdev for both")
print(vspec_amp_snr_df[['peak_time', 'amplitude', 'snr', 'ifo']])

plt.subplot(2, 1, 1)
plt.scatter(amp_snr_df['peak_time'], amp_snr_df['amplitude'])

plt.scatter(upper_amp_snr_df['peak_time'], upper_amp_snr_df['amplitude'], c='r')
plt.ylabel('Amplitude')
plt.xlabel('Peak Time')
plt.scatter(extr_amp_df['peak_time'], extr_amp_df['amplitude'], c='g')
plt.scatter(spec_amp_df['peak_time'], spec_amp_df['amplitude'], c='b')
plt.scatter(vspec_amp_snr_df['peak_time'], vspec_amp_snr_df['amplitude'], c='black')

i = False
for t, A in zip(upper_amp_snr_df['peak_time'], upper_amp_snr_df['amplitude']):
    if i:
        alignment = 'right'
    else:
        alignment = 'left'
    i = not i
    plt.annotate(f"({t:.4g}, {A:.3g})", (t, A), horizontalalignment=alignment)
for t, A in zip(extr_amp_df['peak_time'], extr_amp_df['amplitude']):
    plt.annotate(f"({t:.4g}, {A:.3g})", (t, A))

plt.subplot(2, 1, 2)
plt.scatter(amp_snr_df['peak_time'], amp_snr_df['snr'])
plt.ylabel('Sound to Noise Ratio')
plt.xlabel('Peak Time')
plt.scatter(upper_amp_snr_df['peak_time'], upper_amp_snr_df['snr'], c='r')
plt.scatter(extr_snr_df['peak_time'], extr_snr_df['snr'], c='g')
plt.scatter(spec_snr_df['peak_time'], spec_snr_df['snr'], c='b')
plt.scatter(vspec_amp_snr_df['peak_time'], vspec_amp_snr_df['snr'], c='black')

i = False
for t, y in zip(upper_amp_snr_df['peak_time'], upper_amp_snr_df['snr']):
    if i:
        alignment = 'right'
    else:
        alignment = 'left'
    i = not i
    plt.annotate(f"({t:.4g}, {y:.3g})", (t, y), horizontalalignment=alignment)
for t, y in zip(extr_snr_df['peak_time'], extr_snr_df['snr']):
    plt.annotate(f"({t:.4g}, {y:.3g})", (t, y))

plt.tight_layout()
plt.show()

#print(no_glitch_df['amplitude'].min())
#print(no_glitch_df['amplitude'].max())
#print(no_glitch_df['snr'].min())
#print(no_glitch_df['snr'].max())

#print(no_glitch_df[no_glitch_df['snr']>20]['amplitude'])
samp_total = len(no_glitch_df)

L1_p = len(no_glitch_df[no_glitch_df['ifo']=='L1'])/samp_total
H1_p = len(no_glitch_df[no_glitch_df['ifo']=='H1'])/samp_total

print(f"Percent of L1: {L1_p}")
print(f"Percent of H1: {H1_p}")

print()
print("Mean")
print(f"Amplitude: {no_glitch_df['amplitude'].mean()}")
print(f"SNR: {no_glitch_df['snr'].mean()}")

print()
print("Standard Deviation")
print(f"Amplitude: {no_glitch_df['amplitude'].std()}")
print(f"SNR: {no_glitch_df['snr'].std()}")

print()
print(upper_amp)
print(upper_snr)

