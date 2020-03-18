# NOTE: THIS IS SHIT ...


#
# # def clean_continuum_imagename(
# #     phasecenter,
# #     spw,
# #     scan,
# #     niter,
# #     threshold,
# #     interactive,
# #     mask,
# #     imsize,
# #     cell,
# #     weighting,
# #     robust):
# #     imagename="continuum_"
# #
# #     # ...
# #     imagename+="_phasecenter_"+\
# #         str(phasecenter)+"_"
# #
# #     # ...
# #     imagename+="_spw_"
# #     for i,i_spw in enumerate(spw.split(",")):
# #         if len(i_spw)==1:
# #             imagename+=i_spw
# #             if i<len(spw.split(","))-1:
# #                 imagename+="__"
# #             else:
# #                 imagename+="_"
# #         else:
# #             i_spw_temp=i_spw.split(";")
# #             if len(i_spw_temp)==1:
# #                 _spw_,i_spw_temp_cropped=i_spw_temp[0].split(":")
# #                 i_spw_temp_cropped_split=i_spw_temp_cropped.split("~")
# #                 imagename+=_spw_+\
# #                     "_from_"+i_spw_temp_cropped_split[0]+\
# #                     "_to_"+i_spw_temp_cropped_split[1]+"_"
# #             else:
# #                 k_i=0
# #                 k_j=len(i_spw_temp)-1
# #                 for _i_spw_temp in i_spw_temp:
# #                     if k_i==0:
# #                         _spw_,i_spw_temp_cropped=_i_spw_temp.split(":")
# #                         imagename+=_spw_
# #                     else:
# #                         i_spw_temp_cropped=_i_spw_temp
# #                     i_spw_temp_cropped_split=i_spw_temp_cropped.split("~")
# #                     imagename+="_from_"+i_spw_temp_cropped_split[0]+\
# #                           "_to_"+i_spw_temp_cropped_split[1]
# #                     if k_i<k_j:
# #                         imagename+="_and"
# #                     k_i+=1
# #             imagename+="_"
# #
# #     # ...
# #     if scan:
# #         imagename+="_scan_"
# #         for i_scan in scan.split(","):
# #             imagename+=i_scan+"_"
# #
# #     # ...
# #     if interactive:
# #         pass
# #     else:
# #         imagename+="_iterations_"+str(niter)+"_"
# #
# #         # ...
# #         threshold_value,threshold_units=threshold.split(" ",1)
# #         if threshold_units=="mJy/beam":
# #             imagename+="_threshold_"+threshold_value+"_"
# #         else:
# #             raise ValueError
# #
# #     # ...
# #     if mask:
# #         pass
# #     else:
# #         imagename+="_NoMask_"
# #
# #     # ...
# #     imagename+="_"+str(imsize)+"_"
# #
# #     # ...
# #     cell_value,cell_units=cell.split(" ",1)
# #     if cell_units=="arcsec":
# #         imagename+="_cell_"+cell_value+"_"
# #     else:
# #         raise ValueError
# #
# #     # ...
# #     if weighting in ["natural","uniform"]:
# #         imagename+="_"+weighting
# #     elif weighting=="briggs":
# #         imagename+="_"+weighting+"_robust_"+str(robust)
# #
# #     return imagename
#
#
# def clean_wrapper(
#     vis="",
#     imagename="",
#     field="",
#     phasecenter="",
#     spw="",
#     uvrange="",
#     scan="",
#     niter=0,
#     threshold="0.0 mJy/beam",
#     interactive=False,
#     mask="",
#     imsize=512,
#     cell="1.0 arcsec",
#     weighting="natural",
#     robust=2):
#     #default(clean)
#
#     # ...
#     if field is None or field=="":
#         raise ValueError
#
#     # ...
#     if weighting is None:
#         raise ValueError
#     elif weighting=="natural":
#         robust=2
#     elif weighting=="uniform":
#         robust=-2
#     elif weighting=="briggs":
#         if robust>-2 and robust<2:
#             pass
#         else:
#             raise ValueError
#
#     # ...
#     if niter==0:
#         if threshold=="0.0 mJy/beam":
#             pass
#         else:
#             raise ValueError
#             #threshold="0.0 mJy/beam"
#     else:
#         pass
#         # TODO: Use as a threshold the x1.5 the rms noise of the dirty image (Stach et al. 2018). If that does not exist then create it
#
#     # ...
#     if any(imsize % n == 0 for n in [2,3,5,7]):
#         pass
#     else:
#         raise ValueError
#
#     # ...
#     if cell:
#         pass
#     else:
#         raise ValueError
#
#     # ...
#
#     clean(
#         vis=vis,
#         imagename=imagename,
#         field=field,
#         phasecenter=phasecenter,
#         spw=spw,
#         timerange="",
#         uvrange=uvrange,
#         antenna="",
#         scan=scan,
#         mode="mfs",
#         resmooth=False,
#         niter=niter,
#         threshold=threshold,
#         interactive=False,
#         mask=mask,
#         outframe="LSRK",
#         imsize=imsize,
#         cell=cell,
#         weighting=weighting,
#         robust=robust)
#
# def execute_clean_line():
#     pass
