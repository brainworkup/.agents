# HIPAA Compliance Checklist for Clinical Reports

## 18 HIPAA Identifiers - De-identification Checklist

Verify that ALL of the following identifiers have been removed or altered:

- [ ] **1. Names** - Patient name, family members, healthcare providers (unless necessary and consented)
- [ ] **2. Geographic subdivisions smaller than state**

  - No street addresses
  - No cities (unless >20,000 population and part of ZIP can be kept if >20,000)
  - No counties
  - First 3 digits of ZIP code acceptable only if geographic unit >20,000 people
  - All other portions of ZIP codes removed
- [ ] **3. Dates** (except year)

  - No exact dates of birth (year only acceptable; year of birth for those >89 must be aggregated)
  - No admission dates
  - No discharge dates
  - No dates of service
  - No dates of death
  - Use relative time periods (e.g., "3 months prior") or years only
- [ ] **4. Telephone numbers**

  - No phone numbers of any kind
  - Including patient, family, provider contact numbers
- [ ] **5. Fax numbers**

  - No fax numbers
- [ ] **6. Email addresses**

  - No email addresses for patient or related individuals
- [ ] **7. Social Security numbers**

  - No SSN or partial SSN
- [ ] **8. Medical record numbers**

  - No MRN, hospital ID, or clinic numbers
  - Use coded study ID or case number if needed
- [ ] **9. Health plan beneficiary numbers**

  - No insurance ID numbers
  - No policy numbers
- [ ] **10. Account numbers**

  - No billing account numbers
  - No financial account information
- [ ] **11. Certificate/license numbers**

  - No driver's license numbers
  - No professional license numbers (unless for author credentials)
- [ ] **12. Vehicle identifiers and serial numbers**

  - No license plate numbers
  - No VIN numbers
- [ ] **13. Device identifiers and serial numbers**

  - No pacemaker serial numbers
  - No implant device serial numbers
  - Generic device description acceptable (e.g., "implantable cardioverter-defibrillator")
- [ ] **14. Web URLs**

  - No personal websites
  - No URLs identifying individuals
- [ ] **15. IP addresses**

  - No IP addresses
- [ ] **16. Biometric identifiers**

  - No fingerprints
  - No voiceprints
  - No retinal scans
  - No other biometric data
- [ ] **17. Full-face photographs and comparable images**

  - No full-face photographs without consent
  - Crop or blur faces if showing
  - Remove identifying features (jewelry, tattoos, birthmarks if not clinically relevant)
  - Black bars over eyes NOT sufficient
  - Ensure no reflection or background identification
- [ ] **18. Any other unique identifying characteristic or code**

  - No unique characteristics that could identify individual
  - No rare disease combinations that could identify
  - Consider if combination of remaining data points could identify individual

---

## Additional De-identification Considerations

### Ages and Dates

- [ ] Patients aged ≤89: Exact age or age range acceptable
- [ ] Patients aged >89: Must be aggregated to "90 or older" or ">89 years"
- [ ] Dates: Use only years OR use relative time periods

  - Example: "3 months prior to presentation" instead of "on January 15, 2023"
  - Example: "admitted in 2023" instead of "admitted on March 10, 2023"

### Geographic Information

- [ ] State or country is acceptable
- [ ] Removed specific cities (unless population >20,000 and no other identifying information)
- [ ] Removed hospital/clinic names
- [ ] Use general descriptors: "a community hospital in the Midwest" or "a tertiary care center"

### Rare Conditions and Combinations

- [ ] Consider if very rare disease alone could identify patient
- [ ] Consider if combination of:

  - Age + diagnosis + geographic area + timeframe could identify patient
- [ ] May need to be vague about certain unique details
- [ ] Balance between providing clinical information and protecting privacy

### Images and Figures

- [ ] All patient identifiers removed from image headers/metadata
- [ ] DICOM data stripped
- [ ] Dates removed from images
- [ ] Medical record numbers removed
- [ ] Faces cropped, blurred, or obscured
- [ ] Identifying marks removed or obscured:

  - Tattoos
  - Jewelry
  - Birthmarks or unique scars (if not clinically relevant)
- [ ] Scale bars and annotations do not contain identifying information
- [ ] Background environment de-identified (room numbers, nameplates, etc.)

### Voice and Video

- [ ] No audio recordings with patient voice (unless consent obtained)
- [ ] No video showing identifiable features (unless consent obtained)
- [ ] If video necessary, face must be obscured

---



---

## Safe Harbor vs. Expert Determination

### Safe Harbor Method

- [ ] All 18 identifiers removed
- [ ] No actual knowledge that remaining information could identify individual
- [ ] Most straightforward method
- [ ] Recommended for most clinical reports

### Expert Determination Method

- [ ] Qualified statistician/expert determined very small re-identification risk
- [ ] Methodology documented
- [ ] Analysis methods specified
- [ ] Conclusion documented
- [ ] May allow retention of some data elements
- [ ] Requires statistical expertise

**Method used:** [ ] Safe Harbor  [ ] Expert Determination

---

## Minimum Necessary Standard

### Use and Disclosure

- [ ] Only minimum PHI necessary for purpose is used
- [ ] Purpose of disclosure clearly defined
- [ ] Limited to relevant information only
- [ ] Consider de-identified data or limited data set as alternatives

### Exceptions to Minimum Necessary

Minimum necessary does NOT apply to:

- Treatment purposes (providers may need full information)
- Patient-authorized disclosures
- Disclosures required by law
- Disclosures to HHS for compliance investigation

---

## Documentation to Maintain

Keep on file:

- [ ] Signed patient consent (if applicable)
- [ ] IRB approval (if research)
- [ ] HIPAA waiver (if applicable)
- [ ] De-identification verification
- [ ] Data use agreement (if limited data set)
- [ ] Authorization forms (if applicable)
- [ ] Training records for personnel handling PHI
- [ ] Audit logs

**Retention period:** Minimum 6 years per HIPAA requirement
