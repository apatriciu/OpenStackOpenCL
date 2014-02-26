#ifndef __OPENCLOBJECTSMAPS_H__
#define __OPENCLOBJECTSMAPS_H__
 
/*
Maps to store the dynamic OpenCL objects;
The Objects shall store associations between OpenCL objects and their integer Id. 
The Module uses boost...
*/

// C interface
// devices and platforms
int InitializePlatformAndDevices(void);
long GetNumberOfDevices(void);
void GetDevicesIds(long id[]);
long GetDeviceID(cl_device_id clDevID);
cl_device_id GetCLDevice(long id);
cl_platform_id GetCLPlatform(long id);

// contexts
int InsertContext(cl_context pc, long* context_id);
cl_context GetContext(long id);
int RetainContext(long id);
int ReleaseContext(long id);
long GetContextID(cl_context pc);
long GetNumberOfContexts(void);
void GetContextsIDs(long* id);
// commandqueue
int InsertCommandQueue(cl_command_queue pc, long* command_queue_id);
cl_command_queue GetCommandQueue(long id);
int RetainCommandQueue(long id);
int ReleaseCommandQueue(long id);
long GetCommandQueueID(cl_command_queue pc);
long GetNumberOfCommandQueues(void);
void GetCommandQueuesIDs(long* id);
// mem object
int InsertMem(cl_mem pc, long* mem_id);
cl_mem GetMem(long id);
int RetainMem(long id);
int ReleaseMem(long id);
long GetMemID(cl_mem pc);
long GetNumberOfMems(void);
void GetMemsIDs(long* id);
// program object
int InsertProgram(cl_program pc, long*  program_id);
cl_program GetProgram(long id);
int RetainProgram(long id);
int ReleaseProgram(long id);
long GetProgramID(cl_program pc);
long GetNumberOfPrograms(void);
void GetProgramsIDs(long* id);
// kernel object
int InsertKernel(cl_kernel pc, long* kernel_id);
cl_kernel GetKernel(long id);
int RetainKernel(long id);
int ReleaseKernel(long id);
long GetKernelID(cl_context pc);
long GetNumberOfKernels(void);
void GetKernelsIDs(long* id);

#endif

